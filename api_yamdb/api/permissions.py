from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from users.models import CustomUser


# class IamOrReadOnly(permissions.BasePermission):
#     """Собcтвенник, администратор или только чтение."""

#     def has_permission(self, request, view):
#         return request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.user.is_superuser or request.user.role == 'admin'
#             or obj == request.user
#         )

class IamOrReadOnly(permissions.BasePermission):
    """Собcтвенник, администратор или только чтение."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated:
            return True
        raise PermissionDenied(detail='Unauthorized', code=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser or request.user.role == 'admin' or obj == request.user:
            return True
        raise PermissionDenied(detail='Forbidden', code=status.HTTP_403_FORBIDDEN)


class ChangeAdminOnly(permissions.BasePermission):
    """Изменение доступно только администратору."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == 'admin')
        )

# class ChangeAdminOnly(permissions.BasePermission):
#     """Изменение доступно только администратору."""

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin'):
#             return True
#         raise PermissionDenied(detail='Forbidden', code=status.HTTP_403_FORBIDDEN)


# class StaffOrReadOnly(permissions.BasePermission):
#     """Администратор или только чтение."""

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or (request.user.is_authenticated and request.user.role == 'admin')
#         )

# class StaffOrReadOnly(permissions.BasePermission):
#     """Администратор или только чтение."""

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS or (request.user.is_authenticated and request.user.role == 'admin'):
#             return True
#         raise PermissionDenied(detail='Forbidden', code=status.HTTP_403_FORBIDDEN)
class StaffOrReadOnly(permissions.BasePermission):
    """Администратор или только чтение."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        return False


# class AuthorOrStaffOrReadOnly(permissions.BasePermission):
#     """Автор, модератор, админ или только чтение."""

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or obj.author == request.user
#             or request.user.role in ['moderator', 'admin']
#         )
    
class AuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Автор, модератор, админ или только чтение."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated:
            return True
        raise PermissionDenied(detail='Unauthorized', code=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user or request.user.role in ['moderator', 'admin']:
            return True
        raise PermissionDenied(detail='Forbidden', code=status.HTTP_403_FORBIDDEN)
