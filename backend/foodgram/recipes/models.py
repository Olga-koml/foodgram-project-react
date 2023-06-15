from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель Тегов."""

    name = models.CharField(
        verbose_name='Название', unique=True,
        max_length=settings.MAX_LENGTH_NAME
    )
    color = ColorField(
        default='#FF0000', verbose_name='Цвет в формате HEX', unique=True
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_NAME, unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=settings.MAX_LENGTH_NAME
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения', max_length=settings.MAX_LENGTH_NAME
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
                violation_error_message=(
                    'Уже есть такой ингредиент с такой мерой измерения!'
                    )
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='автор'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиент',
        through='RecipesIngredient',
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_LENGTH_NAME
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True)
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                settings.MIN_VALUE_VALIDATOR,
                message=(f'Время приготовления не может быть меньше'
                         f'{settings.MIN_VALUE_VALIDATOR}'),
                )
            ]
     )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipesIngredient(models.Model):
    """Промежуточная модель, для добавления поля
     количества ингредиентов (amount)."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(
            settings.MIN_VALUE_VALIDATOR,
            message=(f'Количество ингредиентов не может быть меньше'
                     f'{settings.MIN_VALUE_VALIDATOR}')
            )]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'{self.recipe}: {self.ingredient.name}'
                f' - {self.amount} {self.ingredient.measurement_unit}')


class FavoriteRecipe(models.Model):
    """Модель для избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Рецепт уже есть в избранном',
                violation_error_message='Рецепт уже есть в избранном'

            ),
        ]

    def __str__(self):
        return (f'{self.user.username} добавил в '
                f'избранное рецепт: {self.recipe.name}')


class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping',
    )

    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='Рецепт уже есть в списке покупок',
                violation_error_message='Рецепт уже есть в списке покупок'
            ),
        ]

    def __str__(self):
        return (f'{self.user.username} добавил '
                'в список покупок рецепт: {self.recipe.name}')
