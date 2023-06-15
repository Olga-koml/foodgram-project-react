from django.db import transaction
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipesIngredient, Tag
from users.models import User
from users.serializers import CustomCreateUserSerializer, SubscribedFlag

from .utilis import Base64ImageFields, add_ingredients_to_recipe


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )


class RecipesIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов с указанием количества.
    Используется как вложенный для сериализатора рецепта."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipesIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецепта."""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipesIngredientSerializer(
        many=True, source='recipesingredient_set', read_only=True
    )
    author = CustomCreateUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        ]

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and user.shopping.filter(recipe=obj).exists())


class RecipeShortDescriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта с укороченным набором полей."""
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'image', 'cooking_time',
        ]


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для публикация рецепта."""
    ingredients = RecipesIngredientSerializer(
        many=True, source='recipesingredient_set', )
    image = Base64ImageFields()
    author = CustomCreateUserSerializer(read_only=True)
    tags = serializers.ListSerializer(
        child=serializers.CharField()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'ingredients', 'tags', 'image',
            'name', 'author', 'text', 'cooking_time'
        )

    def validate(self, data):
        recipe_ingredients = []
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            recipe_ingredients.append(ingredient.get('id'))
        if len(set(recipe_ingredients)) != len(recipe_ingredients):
            raise serializers.ValidationError(
                'Вы ввели повторяющиеся ингредиенты, исправьте для сохранения рецепта'
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('recipesingredient_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        add_ingredients_to_recipe(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipesingredient_set')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        add_ingredients_to_recipe(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance,
                                context=context).data


class SubscriptionSerializer(UserSerializer, SubscribedFlag):
    """Сериализатор для подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username', 'last_name', 'first_name')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        serializer = RecipeShortDescriptionSerializer(
            recipes, many=True, read_only=True
        )
        return serializer.data
