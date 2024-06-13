from rest_framework import serializers

from lessons.models import Language, Question


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
