from rest_framework import serializers

from lessons.models import Language, Lesson, Progress, Question


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['description']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'answer1', 'answer2', 'answer3', 'correct_answer']


class LessonSerializer(serializers.ModelSerializer):
    questions_of_lesson = QuestionSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['title', 'theory', 'questions_of_lesson']


class ProgressSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(queryset=Language.objects.all(),
                                            slug_field='title')
    last_completed_lesson = serializers.SlugRelatedField(
        queryset=Lesson.objects.all(),
        slug_field='serial_number'
    )

    class Meta:
        model = Progress
        fields = ['tg_user_id', 'language', 'last_completed_lesson',
                  'wrong_answers']


class ProgressCreateSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(queryset=Language.objects.all(),
                                            slug_field='title')
    last_completed_lesson = serializers.IntegerField()

    class Meta:
        model = Progress
        fields = ['tg_user_id', 'language', 'last_completed_lesson']

    def create(self, validated_data):
        language = validated_data.get('language')
        tg_user_id = validated_data.get('tg_user_id')
        slug = f'{language}_{tg_user_id}'

        lesson_number = validated_data.pop('last_completed_lesson')
        lesson = Lesson.objects.get(
            language=language,
            serial_number=lesson_number
        )
        progress = Progress.objects.create(slug=slug,
                                           last_completed_lesson=lesson,
                                           **validated_data)
        return progress

    def to_representation(self, instance):
        return ProgressSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


class ProgressGetUpdateDeleteSerializer(serializers.ModelSerializer):
    tg_user_id = serializers.StringRelatedField(read_only=True)
    language = serializers.StringRelatedField(read_only=True)
    last_completed_lesson = serializers.IntegerField()
    wrong_answers = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Progress
        fields = ['tg_user_id', 'language', 'last_completed_lesson',
                  'wrong_answers']

    def update(self, instance, validated_data):
        lesson_number = validated_data.pop('last_completed_lesson',
                                           instance.last_completed_lesson)
        lesson = Lesson.objects.get(
            language=instance.language,
            serial_number=lesson_number
        )
        instance.last_completed_lesson = lesson

        questions_with_wrong_answers = validated_data.get('wrong_answers')
        if questions_with_wrong_answers:
            for question in questions_with_wrong_answers:
                question = Question.objects.get(lesson=lesson,
                                                serial_number=question)
                instance.wrong_answers.add(question)

        instance.save()

        return instance

    def to_representation(self, instance):
        return ProgressSerializer(
            instance, context={'request': self.context.get('request')}
        ).data
