from django.contrib.auth.base_user import BaseUserManager

from api_yamdb.const import (
    SUPER_ADMIN_ROLE,
    USER_ROLE,
)


class YamdbUserManager(BaseUserManager):
    """Переопределяем создание пользователя."""

    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', USER_ROLE)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('role', SUPER_ADMIN_ROLE)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)
