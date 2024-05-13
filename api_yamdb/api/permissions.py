from rest_framework import permissions


class IamOrReadOnly(permissions.BasePermission):
    """Собcтвенник, администратор или только чтение."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser or request.user.role == 'admin'
            or obj == request.user
        )


class ChangeAdminOnly(permissions.BasePermission):
    """Изменение доступно только администратору."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == 'admin')
        )


class StaffOrReadOnly(permissions.BasePermission):
    """Администратор или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )


class AuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Автор, модератор, админ или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        print ('автор= ',obj.author, ' user= ',request.user)
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ['moderator', 'admin']
        )
