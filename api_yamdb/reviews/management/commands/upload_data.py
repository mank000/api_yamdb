import csv
import os

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
    'author': ['author', CustomUser]}


def upload_data(file_name, class_name):
    dir = os.getcwd() + '\\static\\data'
    file_name = file_name + '.csv'
    csv_path = os.path.join(dir, file_name)
    with open(csv_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        objects = []
        for row in reader:
            obj = class_name()
            for field, value in row.items():
                if field == 'id':
                    # Проверка уникальности и отсутствия в базе данных.
                    if class_name.objects.filter(pk=value).exists():
                        print(f'Объект с id={value} уже '
                              'существует в базе данных')
                        continue
                    setattr(obj, field, value)
                elif field in FIELD_TO_KEY:
                    # Получение данных из связанных моделей.
                    try:
                        data = FIELD_TO_KEY[field][1].objects.get(pk=value)
                    except FIELD_TO_KEY[field][1].DoesNotExist:
                        print(f'Объект с id={value} не найден в '
                              f'базе данных {FIELD_TO_KEY[field][1]}')
                        continue
                    setattr(obj, FIELD_TO_KEY[field][0], data)
                else:
                    # Остальные поля таблицы.
                    setattr(obj, field, value)
            objects.append(obj)

        for obj in objects:
            try:
                obj.save()
            except Exception as e:
                print('Ошибка при загрузке '
                      f'данных в таблицу {class_name.__name__}: {e}')


class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **options):
        for key, value in CONFORMITY_FILE_TO_CLASS.items():
            self.stdout.write(f'Начало загрузки таблицы "{key}"')
            upload_data(key, value)
            self.stdout.write(f'Успешное завершение загрузки таблицы "{key}"')
