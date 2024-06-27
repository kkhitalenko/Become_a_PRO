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


class LessonSerializer(serializers.Serializer):
    title = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    questions_of_lesson = QuestionSerializer(many=True)


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
