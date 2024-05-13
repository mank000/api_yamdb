from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Переопределяем модель стандартного юзера."""

    ROLE_CHOICES = [
        ("admin", "Администратор"),
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("super_admin", "Суперпользователь")
    ]

    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                'Это поле может содержать только '
                'буквы, цифры и @, ., +, -, _ знаки'
            ),
        ],
    )

    email = models.EmailField('E-mail',
                              unique=True,
                              max_length=254
                              )

    first_name = models.CharField(verbose_name='Имя',
                                  max_length=150
                                  )

    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=150
                                 )

    bio = models.TextField(blank=True,
                           verbose_name="О себе"
                           )

    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default="user",
                            verbose_name="Роль"
                            )
    confirmation_code = models.CharField(max_length=6,
                                         default="",
                                         blank=True,
                                         verbose_name="Код подтверждения"
                                         )

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]
    # objects = CustomUserManager()

    def __str__(self):
        return self.username
