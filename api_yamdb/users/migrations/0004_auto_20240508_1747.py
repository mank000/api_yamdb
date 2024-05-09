# Generated by Django 3.2 on 2024-05-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20240508_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('user', 'Пользователь'), ('moderator', 'Модератор'), ('super_admin', 'Суперпользователь')], default='user', max_length=20, verbose_name='Роль'),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
