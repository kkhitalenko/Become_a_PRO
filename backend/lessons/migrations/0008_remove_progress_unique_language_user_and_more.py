# Generated by Django 4.2.8 on 2024-06-18 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_progress_unique_language_user'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='progress',
            name='unique_language_user',
        ),
        migrations.RemoveField(
            model_name='progress',
            name='tg_user',
        ),
    ]
