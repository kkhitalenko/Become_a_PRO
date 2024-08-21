from django.db import models


class Question(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE,
                               verbose_name='урок',
                               related_name='questions_of_lesson')
    text = models.TextField('Вопрос', max_length=4096)
    answer1 = models.CharField('Вариант 1', max_length=64)
    answer2 = models.CharField('Вариант 2', max_length=64)
    answer3 = models.CharField('Вариант 3', max_length=64)
    correct_answer = models.CharField('Верный ответ', max_length=64)
    serial_number = models.PositiveIntegerField('Номер вопроса в уроке')

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        ordering = ['serial_number']
        indexes = [models.Index(fields=['lesson', 'serial_number'])]
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
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='язык', related_name='lessons')
    title = models.CharField('Урок', max_length=50)
    theory = models.TextField('Теория', max_length=4096)
    serial_number = models.PositiveIntegerField('Номер урока в языке')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['language', 'serial_number']
        constraints = [
            models.UniqueConstraint(
                fields=['language', 'title'],
                name='unique_language_lesson'
            ),
            models.UniqueConstraint(
                fields=['language', 'serial_number'],
                name='unique_language_lessonsnumber'
            )
        ]

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.CharField('Язык', max_length=50, unique=True)
    description = models.TextField('Описание', max_length=4096)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        return self.title


class Progress(models.Model):
    tg_user_id = models.PositiveBigIntegerField('id пользователя')
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name='язык')
    last_completed_lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT,
                                              verbose_name='последний \
                                                завершенный урок')
    wrong_answers = models.ManyToManyField(Question, blank=True,
                                           verbose_name='вопросы, на которые \
                                            пользователь ответил неверно')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'прогресс пользователя'
        verbose_name_plural = 'прогрессы пользователей'
        indexes = [models.Index(fields=['language', 'tg_user_id'])]
        constraints = [
            models.UniqueConstraint(
                fields=['language', 'tg_user_id'],
                name='unique_language_tguser'
            ),
        ]

    def __str__(self):
        return f'Последний пройденный урок в {self.language} - \
            {self.last_completed_lesson}'
