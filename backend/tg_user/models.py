from django.db import models

from lessons.models import Progress


class TelegramUser(models.Model):
    tg_user_id = models.PositiveBigIntegerField('id пользователя', unique=True)
    progress = models.ManyToManyField(Progress, blank=True,
                                      verbose_name='прогрессы пользователя',
                                      related_name='tguser')

    class Meta:
        verbose_name = 'пользователь бота'
        verbose_name_plural = 'пользователи бота'

    def __str__(self):
        return f'{self.tg_user_id}'
