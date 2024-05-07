from django.contrib.auth.models import AbstractUser
from django.db import models

roles = [
    'user',
    'moderator',
    'admin',
    'super_admin'
]

class CustomUser(AbstractUser):
    role = models.SlugField("Роль", blank=True)
