from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from rest_framework.serializers import ValidationError

from api_yamdb.const import (
    BLOCKED_WORD,
    MAX_LENGTH_CONFCODE,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_TEXT,
    ROLE_CHOICES,
)
from users.managers import YamdbUserManager

ROLE = [
    (ROLE_CHOICES[0], "Администратор"),
    (ROLE_CHOICES[1], "Пользователь"),
    (ROLE_CHOICES[2], "Модератор"),
    (ROLE_CHOICES[3], "Суперадмин")
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
        choices=ROLE,
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
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def validate_username(self, value):
        if value == BLOCKED_WORD:
            raise ValidationError("'me' нельзя использовать.")
        return value

    @property
    def is_admin(self):
        return (self.role == ROLE_CHOICES[0])

    @property
    def is_user(self):
        return (self.role == ROLE_CHOICES[1])

    @property
    def is_moderator(self):
        return (self.role == ROLE_CHOICES[2])

    def __str__(self):
        return self.username
