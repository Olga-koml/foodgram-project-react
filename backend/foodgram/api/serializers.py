from rest_framework import serializers
from .utilis import Base64ImageFields
from recipes.models import Ingredient, Recipe, Tag, RecipesIngredient, FavoriteRecipe
from django.shortcuts import get_object_or_404
from django.db import transaction
from users.serializers import CustomCreateUserSerializer, SubscribedFlag
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from users.models import User, Subscription
from djoser.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        #read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )


class RecipesIngredientSerializer(serializers.ModelSerializer):
    #id = serializers.ReadOnlyField(source='ingredient.id')
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    
    class Meta:
        model = RecipesIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount',
        )
        #read_only_fields = ('name', 'measurement_unit')
      

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipesIngredientSerializer(
        many=True, source='recipesingredient_set', read_only=True)
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
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'image', 'cooking_time',
        ]


class RecipePostSerializer(serializers.ModelSerializer):
    
    ingredients = RecipesIngredientSerializer(
        many=True, source='recipesingredient_set', )
    image = Base64ImageFields(required=False, allow_null=True) #переделать на обязательное поле
    author = CustomCreateUserSerializer(read_only=True)
    # tags = serializers.PrimaryKeyRelatedField(many=True,
    #                                           queryset=Tag.objects.all())
    tags = serializers.ListSerializer(
        child=serializers.CharField()
    )
  
    class Meta:
        model = Recipe
        #fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time',)
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'author', 'text', 'cooking_time',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=RecipesIngredient.objects.all(),
        #         fields=['ingredients__resipesingredient__ingredient__name', 'ingredients__ingredient__measurement_unit']
        #     )
        # ]

   

    def validate(self, data): # работает но не дает создать более двух ингредиентов
        ingredients_list = []
        #print('ДАТА', data)
        ingredients = self.initial_data.get('ingredients')
        #print('ПЕЧАТЬ ИНГРЕДИЕНТОВ', ingredients)
        for ingredient in ingredients:
          #  print(ingredient)
           # print('ингредиент гет айди', ingredient.get('id'))
            ingredients_list.append(ingredient.get('id'))
        #print('ингредиент лист', ingredients_list)
        if len(set(ingredients_list)) != len(ingredients_list):
            raise serializers.ValidationError(
                'Вы ввели повторяющиеся ингредиенты, исправьте для сохранения рецепта'
            )
        return data
    

 
    @transaction.atomic # !!!!!!!!!!РАБОЧИЙ МОЙ варинат для админки и постмана
    def create(self, validated_data):
        ingredients = validated_data.pop('recipesingredient_set')
        tags = validated_data.pop('tags')
        # author = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data)
        # recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(Ingredient, id=ingredient['ingredient']['id'])
            #  curent_ingredient = Ingredient.objects.get(id=ingredient['ingredient']['id'])
            # amount = ingredient.get('amount')
            RecipesIngredient.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=ingredient['amount'])
        
        return recipe
    
  
    
    @transaction.atomic  #РАБОЧИЙ вариант
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipesingredient_set')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
     
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(Ingredient, id=ingredient['ingredient']['id'])
            # amount = ingredient.get('amount')
            RecipesIngredient.objects.create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=ingredient['amount'])
   
        return super().update(instance, validated_data)
    
        # @transaction.atomic
    # def update(self, instance, validated_data):
    #     ingredients = validated_data.pop('recipeingredients')
    #     tags = validated_data.pop('tags')
    #     instance.tags.clear()
    #     instance.tags.set(tags)
    #     RecipeIngredient.objects.filter(recipe=instance).delete()
    #     super().update(instance, validated_data)
    #     create_ingredients(ingredients, instance)
    #     instance.save()
    #     return instance

    # def update(self, instance, validated_data):

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     old_tags = RecipeTags.objects.filter(recipe=instance)
    #     old_ingredients = RecipeIngredients.objects.filter(recipe=instance)
    #     old_tags.delete()
    #     old_ingredients.delete()
    #     tags = self.initial_data.get('tags')
    #     ingredients = self.initial_data.get('ingredients')
    #     for tag in tags:
    #         tag = get_object_or_404(Tag, id=tag)
    #         RecipeTags.objects.create(recipe=instance, tag=tag)
    #     for ingredient in ingredients:
    #         id = ingredient.get('id')
    #         amount = ingredient.get('amount')
    #         ingredient_id = get_object_or_404(Ingredient, id=id)
    #         RecipeIngredients.objects.create(
    #             recipe=instance, ingredient=ingredient_id, amount=amount
    #         )
    #     return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance,
                                context=context).data



class SubscriptionSerializer(UserSerializer, SubscribedFlag):
    """Serializer class for model Follow."""
    # fanatic = serializers.SlugRelatedField(
    #     read_only=True, slug_field='username',
    #     default=serializers.CurrentUserDefault()
    # )
    # idol = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all()
    # )
    #idol = CustomCreateUserSerializer(read_only=True)
    # is_subscribed = serializers.SerializerMethodField()
    # is_subscribed = CustomCreateUserSerializer(read_only=True)
    #recipes = RecipeShortDescriptionSerializer(many=True) # Проверить как  повлияет
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()



    # def validate(self, data):
    #     if self.context['request'].user == data['following']:
    #         raise ValidationError(
    #             detail='Пользователь не может подписаться сам на себя'
    #         )
    #     return data

   # class Meta(CustomCreateUserSerializer.Meta):
    class Meta():
        model = User
        
        
        #model = User #Subscription
        # fields = tuple(User.REQUIRED_FIELDS) + (
        #     'recipes', 'recipes_count'
        # )
        fields = ('email', 'id', 'username', 'first_name', 
            'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'last_name', 'first_name')
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Subscription.objects.all(),
        #         fields=['idol', 'fanatic'],
        #         message='Вы HHHHHHHHHHя'
        #     )
        # ]


    def get_recipes_count(self, obj):
      #  print('ПЕЧАТЬ!!!', obj) #УДАЛИТЬ ПОТОМ!!!
        # return obj['recipes_count']
        # return obj.idol.recipes.count() # ПРОВЕРИТЬ ЭТОТ ВАРИНТ
        return obj.recipes.count()
   
    def get_recipes(self, obj):
    #     request = self.context.get('request')
    #     limit = request.GET.get('recipes_limit')
    #     print(obj, "ОБЖЕКТ!!!!!!!!!!")
    #     queryset = Recipe.objects.filter(author=obj.idol)
    #    # queryset_recipes = obj.recipes.all()
    #    # queryset = recipes.filter(idol=obj)
    #    # queryset = obj.recipes.filter(idol=obj)
    #     if limit:
    #         queryset = queryset[:int(limit)]
    #     serializer = RecipeShortDescriptionSerializer(queryset, many=True) # read_only = True????
    #     return serializer.data
    #
        recipes = obj.recipes.all()
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortDescriptionSerializer(recipes, many=True, read_only=True)
        return serializer.data
    #

    # def validate(self, data):
    #     for key, value in data.items():
    #         print(key, ':', value)
      
    #     print('DKFJLSDKFJSLDFK', data )
    #     print(self.context['request'].user, 'kjslkdjf')
    #     if self.context['request'].user == data['idol_user']:
    #         raise ValidationError(
    #             detail='Пользователь не может подписаться сам на себя'
    #         )
    #     return data
    # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     context = {'request': request}
    #     return RecipeShortDescriptionSerializer(instance,
    #                             context=context).data
