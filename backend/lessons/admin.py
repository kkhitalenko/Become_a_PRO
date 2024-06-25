from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from lessons.models import Language, Lesson, Progress, Question


def get_link(obj, qty: int, category: str, subcategory: str):
    """Возвращает ссылку на страницу с subcategory, отфильтрованными по
    category."""

    url = (reverse(f'admin:lessons_{subcategory}_changelist') + '?' +
           urlencode({f'{category}__id': f'{obj.id}'}))
    return format_html('<a href="{}">{}</a>', url, qty)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'correct_answer', 'serial_number', 'lesson',
                    'language']
    list_filter = ['lesson', 'lesson__language']
    list_display_links = ['text']
    search_fields = ['text']
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('lesson', 'text', 'serial_number')
        }),
        ('Ответ', {
            'fields': ('answer1', 'answer2', 'answer3', 'correct_answer')
        }),
    )

    @admin.display(description='Язык')
    def language(self, obj):
        return obj.lesson.language


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'language', 'serial_number',
                    'questions_qty']
    list_display_links = ['title']
    list_filter = ['language']
    search_fields = ['title']
    list_per_page = 20

    @admin.display(description='Вопросы')
    def questions_qty(self, obj):
        qty = Question.objects.filter(lesson=obj).count()
        return get_link(obj, qty, 'lesson', 'question')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'lessons_qty']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ('title', )}

    @admin.display(description='Уроки')
    def lessons_qty(self, obj):
        qty = Lesson.objects.filter(language=obj).count()
        return get_link(obj, qty, 'language', 'lesson')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['tg_user_id', 'language', 'last_completed_lesson']
