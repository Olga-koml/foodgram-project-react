from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q

User = get_user_model()


class Subscription(models.Model):
    """Модель подписок"""
    fanatic = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fanatic',
        verbose_name='Подписчик'
    )
    idol = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='idol',
        verbose_name='Автор рецепта'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fanatic', 'idol'], name='unique_subscription',
                violation_error_message='Вы уже подписаны на данного автора!'
            ),
            models.CheckConstraint(
                check=~Q(idol=F('fanatic')),
                name='idol_is_not_fan',
                violation_error_message='Нельзя подписаться на самого себя!'
            )
        ]
