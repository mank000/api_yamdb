# from django.contrib.auth.base_user import BaseUserManager


# class CustomUserManager(BaseUserManager):
#     """Переопределяем создание суперпользователя"""

#     def create_user(self, username, email, **extra_fields):
#         extra_fields.setdefault('role', 'user')
#         return self.model.objects.create(
#             username=username,
#             email=email,
#             **extra_fields
#         )

#     def create_superuser(self, username, email, **extra_fields):
#         extra_fields.setdefault('role', 'super_admin')
#         return self.create_user(username, email, **extra_fields)
