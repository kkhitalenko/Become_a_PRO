from rest_framework import serializers

from lessons.models import Answer, Language, Lesson, Question, Topic


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name', 'description']


class TopicSerializer(serializers.ModelSerializer):
    language = serializers.CharField()

    class Meta:
        model = Topic
        fields = ['language', 'name']


class LessonSerializer(serializers.ModelSerializer):
    topic = serializers.CharField()

    class Meta:
        model = Lesson
        fields = ['topic', 'name', 'theory']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer 
        fields = ['text']


class QuestionSerializer(serializers.ModelSerializer):
    lesson = serializers.CharField()
    options = AnswerSerializer(many=True)
    correct_option = serializers.CharField()

    class Meta:
        model = Question
        fields = ['lesson', 'text', 'options', 'correct_option']
