from rest_framework import serializers

from lessons.models import Language, Progress, Question


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['description']


class QuestionSerializer(serializers.ModelSerializer):
    lesson = serializers.CharField()
    options = serializers.StringRelatedField(many=True)
    correct_option = serializers.CharField()

    class Meta:
        model = Question
        fields = ['lesson', 'text', 'options', 'correct_option']


class ProgressSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(queryset=Language.objects.all(),
                                            slug_field='title')

    class Meta:
        model = Progress
        fields = ['tg_user_id', 'language', 'last_completed_lesson',
                  'wrong_answers']
