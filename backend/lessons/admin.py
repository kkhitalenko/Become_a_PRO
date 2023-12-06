from django.contrib import admin

from lessons.models import Answer, Language, Lesson, Question, Topic


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'correct_option']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
