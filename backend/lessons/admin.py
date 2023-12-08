from django.contrib import admin
from lessons.models import Answer, Language, Lesson, Question, Topic


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'correct_option', 'lesson', 'topic',
                    'language']
    list_filter = ['lesson']

    @admin.display(description='Тема')
    def topic(self, obj):
        return (obj.lesson.topic)

    @admin.display(description='Язык')
    def language(self, obj):
        return (obj.lesson.topic.language)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'questions_qty', 'topic', 'language']
    list_filter = ['topic']

    @admin.display(description='Язык')
    def language(self, obj):
        return (obj.topic.language)

    @admin.display(description='Количество вопросов')
    def questions_qty(self, obj):
        return (Question.objects.filter(lesson=obj)).count()


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lessons_qty', 'language']
    list_filter = ['language']

    @admin.display(description='Количество уроков')
    def lessons_qty(self, obj):
        return (Lesson.objects.filter(topic=obj)).count()


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'topics_qty']

    @admin.display(description='Количество тем')
    def topics_qty(self, obj):
        return (Topic.objects.filter(language=obj)).count()
