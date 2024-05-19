from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.const import (
    MAX_LENGTH_CONFCODE,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_TEXT,
    ADMIN_ROLE,
    MODERATOR_ROLE,
    USER_ROLE,
)
from users.managers import YamdbUserManager
from .validators import validate_no_me

ROLE = [
    (ADMIN_ROLE, "Администратор"),
    (USER_ROLE, "Пользователь"),
    (MODERATOR_ROLE, "Модератор"),
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
            validate_no_me
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
        default=USER_ROLE,
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

    @property
    def is_admin(self):
        return (self.role == ADMIN_ROLE)

    @property
    def is_moderator(self):
        return (self.role == MODERATOR_ROLE)

    def __str__(self):
        return self.username
