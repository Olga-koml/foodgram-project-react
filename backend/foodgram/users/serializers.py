from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import User


class SubscribedFlag(serializers.Serializer):
    """Вспомогательный класс для отображения поля is_subscribed
    у пользователя. Используется в нескольких сериализаторах."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and
                user.fanatic.filter(idol=obj).exists())


class CustomCreateUserSerializer(UserCreateSerializer, SubscribedFlag):
    """Сериализатор для изменения отображения встроенных полей пользователя."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password', 'is_subscribed'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
