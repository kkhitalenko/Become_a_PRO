from django.db import models


class Answer(models.Model):
    text = models.CharField(max_length=50, unique=True, verbose_name='Ответ')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.TextField(verbose_name='Вопрос')
    options = models.ManyToManyField(Answer, verbose_name='Варианты ответа',
                                     related_name='options')
    correct_option = models.ForeignKey(Answer, on_delete=models.PROTECT,
                                       verbose_name='Верный ответ',
                                       related_name='correct_option')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тема урока')
    theory = models.TextField(verbose_name='Теория')
    questions = models.ManyToManyField(Question, verbose_name='Вопросы',
                                       related_name='questions_from_lesson',
                                       blank=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тема')
    lessons = models.ManyToManyField(Lesson, verbose_name='Уроки',
                                     related_name='lessons_from_topic',
                                     blank=True)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Язык')
    description = models.TextField(verbose_name='Описание')
    topics = models.ManyToManyField(Topic, verbose_name='Темы',
                                    related_name='topics_from_language',
                                    blank=True)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        return self.name
