# Generated by Django 4.2.13 on 2024-07-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0011_alter_lesson_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
