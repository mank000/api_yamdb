# Команда, заполняющая таблицу users_role
# Использовать при утере базы данных!
# python manage.py command
from django.core.management.base import BaseCommand
from users.models import Role


class Command(BaseCommand):
    help = 'Заполнить таблицу существующими ролями.'

    def handle(self, *args, **kwargs):
        for role_key, role_name in Role.ROLE_CHOICES:
            Role.objects.get_or_create(name=role_key)