from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс для настройки всех прав автору,
    и только чтения для остальных пользователей"""
    message = 'Изменение и удаление запрещено! Вы не являетесь автором рецепта'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
