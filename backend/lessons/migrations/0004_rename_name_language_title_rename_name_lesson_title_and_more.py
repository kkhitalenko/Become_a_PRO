# Generated by Django 4.2.8 on 2024-05-27 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_alter_lesson_topic_alter_question_correct_option_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='language',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='language',
            name='slug',
            field=models.SlugField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='serial_number',
            field=models.PositiveIntegerField(default=1, verbose_name='Номер урока в теме'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='serial_number',
            field=models.PositiveIntegerField(default=1, verbose_name='Номер вопроса в уроке'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='serial_number',
            field=models.PositiveIntegerField(default=1, verbose_name='Номер темы в языке'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=255, unique=True, verbose_name='Ответ'),
        ),
        migrations.AddConstraint(
            model_name='lesson',
            constraint=models.UniqueConstraint(fields=('topic', 'title'), name='unique_topic_lesson'),
        ),
        migrations.AddConstraint(
            model_name='lesson',
            constraint=models.UniqueConstraint(fields=('topic', 'serial_number'), name='unique_topic_lessonsnumber'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('lesson', 'text'), name='unique_lesson_question'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('lesson', 'serial_number'), name='unique_lesson_questionssnumber'),
        ),
        migrations.AddConstraint(
            model_name='topic',
            constraint=models.UniqueConstraint(fields=('language', 'title'), name='unique_language_topic'),
        ),
        migrations.AddConstraint(
            model_name='topic',
            constraint=models.UniqueConstraint(fields=('language', 'serial_number'), name='unique_language_topicsnumber'),
        ),
    ]
