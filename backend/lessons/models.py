from django.db import models


class Answer(models.Model):
    text = models.CharField('Ответ', max_length=255, unique=True)

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
    serial_number = models.PositiveIntegerField('Номер вопроса в уроке')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        constraints = [
            models.UniqueConstraint(
                fields=['lesson', 'text'], name='unique_lesson_question'
            ),
            models.UniqueConstraint(
                fields=['lesson', 'serial_number'],
                name='unique_lesson_questionssnumber'
            )
        ]

    def __str__(self):
        return self.text


class Lesson(models.Model):
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE,
                              verbose_name='Тема', related_name='lessons')
    title = models.CharField('Урок', max_length=50)
    theory = models.TextField('Теория')
    serial_number = models.PositiveIntegerField('Номер урока в теме')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        constraints = [
            models.UniqueConstraint(
                fields=['topic', 'title'], name='unique_topic_lesson'
            ),
            models.UniqueConstraint(
                fields=['topic', 'serial_number'],
                name='unique_topic_lessonsnumber'
            )
        ]

    def __str__(self):
        return self.title


class Topic(models.Model):
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык', related_name='topics')
    title = models.CharField('Тема', max_length=50)
    serial_number = models.PositiveIntegerField('Номер темы в языке')

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        constraints = [
            models.UniqueConstraint(
                fields=['language', 'title'], name='unique_language_topic'
            ),
            models.UniqueConstraint(
                fields=['language', 'serial_number'],
                name='unique_language_topicsnumber'
            )
        ]

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.CharField('Язык', max_length=50, unique=True)
    description = models.TextField('Описание')
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        return self.title
