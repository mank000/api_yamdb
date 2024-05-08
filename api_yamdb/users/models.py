from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Переопределяем модель стандартного юзера."""

    ROLE_CHOICES = [
        ("admin", "Администратор"),
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("super_admin", "Суперпользователь")
    ]

    # Поле для роли.
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default="user")

    def save(self, *args, **kwargs):
        """Переопределяем метод save для автоматического присваивания роли."""
        if not self.pk:
            # Можно изменить значение по умолчанию для роли
            self.role = "user"
        super().save(*args, **kwargs)
