from django.db import models


class Answer(models.Model):
    text = models.CharField('Ответ', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text


class Question(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE,
                               verbose_name='Урок',
                               related_name='questions_of_lesson')
    text = models.TextField('Вопрос')
    options = models.ManyToManyField(Answer, verbose_name='Варианты ответа')
    correct_option = models.ForeignKey(Answer, on_delete=models.PROTECT,
                                       verbose_name='Верный ответ',
                                       related_name='questions_correct_option')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Lesson(models.Model):
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE,
                              verbose_name='Тема', related_name='lessons')
    name = models.CharField('Урок', max_length=50)
    theory = models.TextField('Теория')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class Topic(models.Model):
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык', related_name='topics')
    name = models.CharField('Тема', max_length=50)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField('Язык', max_length=50, unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        return self.name
