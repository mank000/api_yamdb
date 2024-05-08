from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """Класс ролей."""
    ROLE_CHOICES = [
        ("admin", "Администратор"),
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("super_admin", "Суперпользователь")
    ]

    name = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            unique=True,
                            )

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Переопределяем модель стандартного юзера."""
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        """Переопределяем метод save для автоматического присваивания user."""
        if not self.pk:
            self.role = Role.objects.get(name="user")
        super().save(*args, **kwargs)
