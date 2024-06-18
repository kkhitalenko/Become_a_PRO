from django.contrib import admin

from tg_user.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user_id']
    list_per_page = 20
