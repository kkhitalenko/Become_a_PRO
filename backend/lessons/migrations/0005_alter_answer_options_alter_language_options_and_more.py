# Generated by Django 4.2.8 on 2024-06-11 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_rename_name_language_title_rename_name_lesson_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'ответ', 'verbose_name_plural': 'ответы'},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'язык', 'verbose_name_plural': 'языки'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'вопрос', 'verbose_name_plural': 'вопросы'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name': 'тема', 'verbose_name_plural': 'темы'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='lessons.topic', verbose_name='тема'),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions_correct_option', to='lessons.answer', verbose_name='верный ответ'),
        ),
        migrations.AlterField(
            model_name='question',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_of_lesson', to='lessons.lesson', verbose_name='урок'),
        ),
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.ManyToManyField(to='lessons.answer', verbose_name='варианты ответа'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='lessons.language', verbose_name='язык'),
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.language', verbose_name='язык')),
                ('last_completed_lesson', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lessons.lesson', verbose_name='пройденный урок')),
                ('tg_user', models.PositiveBigIntegerField(verbose_name='id пользователя бота')),
                ('wrong_answers', models.ManyToManyField(blank=True, to='lessons.question', verbose_name='неверные ответы')),
            ],
            options={
                'verbose_name': 'прогресс',
                'verbose_name_plural': 'прогрессы',
            },
        ),
    ]
