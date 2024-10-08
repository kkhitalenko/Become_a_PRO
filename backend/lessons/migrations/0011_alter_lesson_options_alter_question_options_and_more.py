# Generated by Django 4.2.13 on 2024-06-27 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0010_remove_topic_language_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['language', 'serial_number'], 'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['serial_number'], 'verbose_name': 'вопрос', 'verbose_name_plural': 'вопросы'},
        ),
        migrations.AlterOrderWithRespectTo(
            name='lesson',
            order_with_respect_to=None,
        ),
        migrations.AlterOrderWithRespectTo(
            name='question',
            order_with_respect_to=None,
        ),
    ]
