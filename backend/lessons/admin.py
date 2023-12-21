from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from lessons.models import Answer, Language, Lesson, Question, Topic


def get_link(obj, qty: int, category: str, subcategory: str):
    """Возвращает ссылку на страницу с subcategory, отфильтрованными по
    category."""

    url = (reverse(f'admin:lessons_{subcategory}_changelist') + '?' +
           urlencode({f'{category}__id': f'{obj.id}'}))
    return format_html('<a href="{}">{}</a>', url, qty)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_display_links = ['id', 'text']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'correct_option', 'lesson', 'topic',
                    'language']
    # list_filter = ['lesson']
    list_display_links = ['id', 'text']

    @admin.display(description='Тема')
    def topic(self, obj):
        return obj.lesson.topic

    @admin.display(description='Язык')
    def language(self, obj):
        return obj.lesson.topic.language


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'questions_qty', 'topic', 'language']
    list_display_links = ['id', 'name']
    list_filter = ['topic']

    @admin.display(description='Язык')
    def language(self, obj):
        return obj.topic.language

    @admin.display(description='Количество вопросов')
    def questions_qty(self, obj):
        qty = Question.objects.filter(lesson=obj).count()
        return get_link(obj, qty, 'lesson', 'question')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lessons_qty', 'language']
    list_display_links = ['id', 'name']
    list_filter = ['language']

    @admin.display(description='Количество уроков')
    def lessons_qty(self, obj):
        qty = Lesson.objects.filter(topic=obj).count()
        return get_link(obj, qty, 'topic', 'lesson')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'topics_qty']
    list_display_links = ['id', 'name']

    @admin.display(description='Количество тем')
    def topics_qty(self, obj):
        qty = Topic.objects.filter(language=obj).count()
        return get_link(obj, qty, 'language', 'topic')
