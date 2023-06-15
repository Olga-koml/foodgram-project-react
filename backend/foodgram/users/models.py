from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q

User = get_user_model()


class Subscription(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор рецепта'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription',
                violation_error_message='Вы уже подписаны на данного автора!'
            ),
            models.CheckConstraint(
                check=~Q(author=F('user')),
                name='author_is_not_subscriber',
                violation_error_message='Нельзя подписаться на самого себя!'
            )
        ]
