from django.db import models


class TelegramUser(models.Model):
    tg_user_id = models.PositiveBigIntegerField('id пользователя', unique=True)
    username = models.CharField('Имя пользователя', max_length=255, blank=True,
                                null=True)

    class Meta:
        verbose_name = 'пользователь бота'
        verbose_name_plural = 'пользователи бота'

    def __str__(self):
        return f'{self.tg_user_id}'
