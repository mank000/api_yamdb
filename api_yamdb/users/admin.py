from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

UserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент — это название раздела в админке,
    # а второй элемент — словарь, где под ключом fields можно указать нужные поля.
    ('Extra Fields', {'fields': ('role',)}),
)

admin.site.register(CustomUser, UserAdmin)