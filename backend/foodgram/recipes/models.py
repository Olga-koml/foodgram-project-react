from django.db import models
from django.core.validators import MinValueValidator
from colorfield.fields import ColorField
#from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(verbose_name='Название', unique=True, max_length=200)
    #color = models.CharField(max_length=7, verbose_name='Цвет', unique=True)
    color = ColorField(default='#FF0000', verbose_name='Цвет в формате HEX', unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент', max_length=200)
    measurement_unit = models.CharField(verbose_name='Единица измерения', max_length=200)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], 
                name='unique_ingredient',
                violation_error_message='Уже есть такой ингредиент с такой мерой измерения!'
                                    )
        ]
        
    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        # blank=True,
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='автор')

    ingredients = models.ManyToManyField(
        Ingredient,
        #blank=True,
        verbose_name='Ингридиент',
        through='RecipesIngredient',
        related_name='recipes',
    )
    
    name = models.CharField(verbose_name='Название', max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True)
    text = models.TextField(verbose_name='Описание')
    # tag = models.ForeignKey(
    #     Tag,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='recipes',
    #     verbose_name='тег'
    # )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1, message='Время приготовления не может быть меньше 1', )]
     )
    
    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
    

class RecipesIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        )
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='Ингредиент', 
        on_delete=models.CASCADE,
        )
    amount = models.PositiveIntegerField(
        verbose_name='Количество', validators=[MinValueValidator(
            1, message='Количество ингредиентов не может быть меньше 1'
            )]
        )
    
    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}' 


# class ShoppingCart(models.Model):
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE,
#         )

class FavoriteRecipe(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        #null=True,
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
        # ordering = ['-id'] надо ли тут сортировка?

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
        return f'{self.user.username} добавил в избранное рецепт: {self.recipe.name}'
       


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        #null=True,
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
        # ordering = ['-id'] надо ли тут сортировка?

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
        return f'{self.user.username} добавил в список покупок рецепт: {self.recipe.name}'
       
