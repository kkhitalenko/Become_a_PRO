from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from lessons.models import Answer, Language, Lesson, Progress, Question, Topic


def get_link(obj, qty: int, category: str, subcategory: str):
    """Возвращает ссылку на страницу с subcategory, отфильтрованными по
    category."""

    url = (reverse(f'admin:lessons_{subcategory}_changelist') + '?' +
           urlencode({f'{category}__id': f'{obj.id}'}))
    return format_html('<a href="{}">{}</a>', url, qty)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text']
    list_display_links = ['text']
    search_fields = ['text']
    list_per_page = 20


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'correct_option', 'lesson', 'topic', 'language']
    list_filter = ['lesson', 'lesson__topic', 'lesson__topic__language']
    list_display_links = ['text']
    search_fields = ['text']
    list_per_page = 20

    @admin.display(description='Тема')
    def topic(self, obj):
        return obj.lesson.topic

    @admin.display(description='Язык')
    def language(self, obj):
        return obj.lesson.topic.language


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'questions_qty', 'topic', 'language']
    list_display_links = ['title']
    list_filter = ['topic', 'topic__language']
    search_fields = ['title']
    list_per_page = 20

    @admin.display(description='Язык')
    def language(self, obj):
        return obj.topic.language

    @admin.display(description='Вопросы')
    def questions_qty(self, obj):
        qty = Question.objects.filter(lesson=obj).count()
        return get_link(obj, qty, 'lesson', 'question')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'lessons_qty', 'language']
    list_display_links = ['title']
    list_filter = ['language']
    search_fields = ['title']
    list_per_page = 20

    @admin.display(description='Уроки')
    def lessons_qty(self, obj):
        qty = Lesson.objects.filter(topic=obj).count()
        return get_link(obj, qty, 'topic', 'lesson')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'topics_qty']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ('title', )}

    @admin.display(description='Темы')
    def topics_qty(self, obj):
        qty = Topic.objects.filter(language=obj).count()
        return get_link(obj, qty, 'language', 'topic')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['language', 'last_completed_lesson']
