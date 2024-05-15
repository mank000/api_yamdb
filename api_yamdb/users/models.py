from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

from rest_framework.serializers import ValidationError

from .const import (
    MAX_LENGTH_TEXT,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_CONFCODE,
    MAX_LENGTH_EMAIL
)
from .managers import YamdbUserManager


ROLE_NAMES = [
    ("Администратор"),
    "Пользователь",
    "Модератор",
]


class YamdbUser(AbstractUser):
    """Переопределяем модель стандартного юзера."""

    username = models.CharField(
        verbose_name='Username',
        max_length=MAX_LENGTH_TEXT,
        unique=True,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                'Это поле может содержать только '
                'буквы, цифры и @, ., +, -, _ знаки'
            ),
        ],
    )

    email = models.EmailField(
        'E-mail',
        unique=True,
        max_length=MAX_LENGTH_EMAIL
    )

    first_name = models.CharField(
        max_length=MAX_LENGTH_TEXT
    )

    last_name = models.CharField(
        max_length=MAX_LENGTH_TEXT
    )

    bio = models.TextField(
        blank=True,
        verbose_name="О себе"
    )

    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        default=ROLE_CHOICES[1],
        verbose_name="Роль"
    )
    confirmation_code = models.CharField(
        max_length=MAX_LENGTH_CONFCODE,
        default="",
        blank=True,
        verbose_name="Код подтверждения"
    )

    objects = YamdbUserManager()

    class Meta:
        verbose_name = "Пользователь"
        ordering = ("username",)

    # Проверить!
    def validate_username(self, value):
        if value == "me":
            raise ValidationError("'me' нельзя использовать.")
        return value

    def is_admin(self):
        ...

    def is_user(self):
        ...

    def is_moderator(self):
        ...

    def __str__(self):
        return self.username
