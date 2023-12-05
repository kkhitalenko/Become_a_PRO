from django.db import models


class Answer(models.Model):
    text = models.CharField(max_length=50, verbose_name='Ответ')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.TextField(verbose_name='Вопрос')
    options = models.ManyToManyField(Answer, related_name='options')
    correct_option = models.ForeignKey(Answer, on_delete=models.PROTECT,
                                       verbose_name='Верный ответ',
                                       related_name='correct_option')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text
