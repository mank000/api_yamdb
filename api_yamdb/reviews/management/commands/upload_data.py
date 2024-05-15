import csv
import os
import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
)
from users.models import CustomUser


User = get_user_model()

CONFORMITY_FILE_TO_CLASS = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': CustomUser,
    'review': Review,
    'comments': Comment
}

FIELD_TO_KEY = {
    'category': ['category', Category],
    'genre_id': ['genre', Genre],
    'title_id': ['title', Title],
    'author': ['author', User]}


def get_static_data_dir():
    return os.path.join(settings.STATICFILES_DIRS[0], 'data')


def get_file_path(file_name):
    static_data_dir = get_static_data_dir()
    return os.path.join(static_data_dir, file_name + '.csv')


def process_row(row, class_name):
    obj = class_name()
    for field, value in row.items():
        if not set_field(obj, field, value, class_name):
            return None
    return obj


def set_field(obj, field, value, class_name):
    if field == 'id':
        if class_name.objects.filter(pk=value).exists():
            sys.stdout.write(f'Объект с id={value} уже существует в базе данных\n')
            return False
        setattr(obj, field, value)
    elif field in FIELD_TO_KEY:
        try:
            data = FIELD_TO_KEY[field][1].objects.get(pk=value)
        except FIELD_TO_KEY[field][1].DoesNotExist:
            sys.stdout.write(f'Объект с id={value}\n'
                  f'не найден в базе данных {FIELD_TO_KEY[field][1]}')
            return False
        setattr(obj, FIELD_TO_KEY[field][0], data)
    else:
        setattr(obj, field, value)
    return True


def upload_data(file_name, class_name):
    file_path = get_file_path(file_name)

    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        objects = []
        for row in reader:
            obj = process_row(row, class_name)
            if obj is not None:
                objects.append(obj)

        for obj in objects:
            try:
                obj.save()
            except Exception as e:
                sys.stdout.write('Ошибка при загрузке данных.\n'
                      f'в таблицу {class_name.__name__}: {e}')


class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **options):
        for key, value in CONFORMITY_FILE_TO_CLASS.items():
            self.stdout.write(f'Начало загрузки таблицы "{key}"')
            upload_data(key, value)
            self.stdout.write(f'Успешное завершение загрузки таблицы "{key}"')
