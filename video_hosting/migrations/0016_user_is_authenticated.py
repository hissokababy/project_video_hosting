# Generated by Django 5.2 on 2025-05-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_hosting', '0015_remove_video_video_creation_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_authenticated',
            field=models.BooleanField(default=True, verbose_name='Авторизованный пользователь'),
        ),
    ]
