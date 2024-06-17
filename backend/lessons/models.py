from django.db import models


class Answer(models.Model):
    text = models.CharField('Ответ', max_length=255, unique=True)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return self.text


class Question(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE,
                               verbose_name='урок',
                               related_name='questions_of_lesson')
    text = models.TextField('Вопрос')
    options = models.ManyToManyField(Answer, verbose_name='варианты ответа')
    correct_option = models.ForeignKey(Answer, on_delete=models.PROTECT,
                                       verbose_name='верный ответ',
                                       related_name='questions_correct_option')
    serial_number = models.PositiveIntegerField('Номер вопроса в уроке')

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        constraints = [
            models.UniqueConstraint(
                fields=['lesson', 'text'],
                name='unique_lesson_question'
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
                              verbose_name='тема', related_name='lessons')
    title = models.CharField('Урок', max_length=50)
    theory = models.TextField('Теория')
    serial_number = models.PositiveIntegerField('Номер урока в теме')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        constraints = [
            models.UniqueConstraint(
                fields=['topic', 'title'],
                name='unique_topic_lesson'
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
                                 verbose_name='язык', related_name='topics')
    title = models.CharField('Тема', max_length=50)
    serial_number = models.PositiveIntegerField('Номер темы в языке')

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'
        # order_with_respect_to = 'language'
        constraints = [
            models.UniqueConstraint(
                fields=['language', 'title'],
                name='unique_language_topic'
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
        verbose_name = 'язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        return self.title


class Progress(models.Model):
    tg_user = models.PositiveBigIntegerField('id пользователя бота')
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name='язык')
    last_completed_lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT,
                                              verbose_name='последний \
                                                завершенный урок')
    wrong_answers = models.ManyToManyField(Question, blank=True,
                                           verbose_name='вопросы, на которые \
                                            пользователь ответил неверно')

    class Meta:
        verbose_name = 'прогресс пользователя'
        verbose_name_plural = 'прогрессы пользователей'

        constraints = [
            models.UniqueConstraint(
                fields=['tg_user', 'language'],
                name='unique_language_user'
            ),
        ]

    def __str__(self):
        return f'Прогресс пользователя {self.tg_user} в {self.language}'
