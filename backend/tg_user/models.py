from django.db import models


class TelegramUser(models.Model):
    tg_user_id = models.PositiveBigIntegerField('id пользователя', unique=True)
    username = models.CharField('Имя пользователя', max_length=255, blank=True,
                                null=True)

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
