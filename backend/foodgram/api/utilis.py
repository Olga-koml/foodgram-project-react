import base64
from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework import status

from recipes.models import Recipe, RecipesIngredient, ShoppingCart
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.shortcuts import HttpResponse
from datetime import datetime as dt
from prettytable import PrettyTable
from django.db import IntegrityError


class Base64ImageFields(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, img_string = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(img_string), name='temp.' + ext)  
        return super().to_internal_value(data)


def add_recipe_to(add_serializer, model, request, recipe_id):
    user = request.user
    try:   
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.create(user=user, recipe=recipe)
        serializer = add_serializer(recipe)
        return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
    
    except IntegrityError as error:
        if 'unique constraint' in str(error): 
            return Response({'errors': str(error).split('"')[1]},
                     status=HTTP_400_BAD_REQUEST)
        
  
# def add_recipe_to(add_serializer, model, request, recipe_id):
#     user = request.user
#     if model.objects.filter(user=user, recipe__id=recipe_id).exists():
#         return Response({'errors': 'Рецепт уже есть в избранном'},
#                         status=HTTP_400_BAD_REQUEST)
  
   
#     # data = {'user': user,
#     #         'recipe': recipe_id}
#     recipe = get_object_or_404(Recipe, id=recipe_id)
#     model.objects.create(user=user, recipe=recipe)
#     serializer = add_serializer(recipe)
#     # serializer = add_serializer(data=data, context={'request': request})
#     # serializer.is_valid(raise_exception=True)
#     # serializer.save()
#     return Response(serializer.data,
#                              status=status.HTTP_201_CREATED)

def del_recipe_from(model, request, recipe_id):
    """Опция добавления и удаления рецепта."""
    user = request.user
    obj = model.objects.filter(user=user, recipe__id=recipe_id)
    if obj.exists():
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'errors': 'Рецепт уже удален!'},
                    status=status.HTTP_400_BAD_REQUEST)
    

# def get_download_shopping_chart(request):
#     user = request.user
#     if not user.shopping.exists():
#         return Response(status=HTTP_400_BAD_REQUEST)
#     recipes = ShoppingCart.objects.filter(recipe__shopping__user=request.user)
#     recipes = recipes.values('recipe__name')
    
#     ingredients = RecipesIngredient.objects.filter(
#         recipe__shopping__user=request.user
#     ).values(
#         'ingredient__name',
#         'ingredient__measurement_unit'
#     ).annotate(amount=Sum('amount'))
#     today = dt.today()
#     shopping_list = (
#         f'Список покупок для пользователя: {user.get_full_name()}\n\n'
#         f'Дата: {today:%Y-%m-%d}\n\n'
#         f'Для приготовления следующих рецептов:\n'
#     )
#     shopping_list += '\n'.join([
#         f'- {recipe["recipe__name"]} '
#         for recipe in recipes
#     ])    
#     shopping_list += f'\n\nНеобходимы следующие ингредиенты:'
#     for order_number, ingredient in enumerate(ingredients):
#         shopping_list += (
#             f'\n{order_number+1}. {ingredient["ingredient__name"]} '
#             f'({ingredient["ingredient__measurement_unit"]})'
#             f' - {ingredient["amount"]} □'
#         ) 
#     shopping_list += f'\n\nИтого {len(ingredients)} ингредиентов для {len(recipes)} рецептов:'       
#     shopping_list += f'\n\nFoodgram ({today:%Y})'
#     filename = f'{user.username}_shopping_list.txt'
#     response = HttpResponse(shopping_list, content_type='text/plain')
#     response['Content-Disposition'] = f'attachment; filename={filename}'
#     return response

def get_download_shopping_chart(request):
    user = request.user
    if not user.shopping.exists():
        return Response(status=HTTP_400_BAD_REQUEST)
    recipes = ShoppingCart.objects.filter(recipe__shopping__user=request.user)
    recipes = recipes.values('recipe__name')
    
    ingredients = RecipesIngredient.objects.filter(
        recipe__shopping__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    today = dt.today()
    shopping_list = (
        f'Список покупок для пользователя: {user.get_full_name()}\n\n'
        f'Дата: {today:%Y-%m-%d}\n\n'
        f'Для приготовления следующих рецептов:\n'
    )
    shopping_list += '\n'.join([
        f'- {recipe["recipe__name"]} '
        for recipe in recipes
    ])    
    shopping_list += f'\n\nНеобходимы следующие ингредиенты:'
    header_ing = ['№', 'Ингредиент', 'мера изм.', 'Количество', 'Чек']
    ing_list = []

    for order_number, ingredient in enumerate(ingredients):
        ing_list.append(f'{order_number+1}.')
        ing_list.append(f'{ingredient["ingredient__name"]} ')
        ing_list.append(f'({ingredient["ingredient__measurement_unit"]})')
        ing_list.append(f'{ingredient["amount"]}')
        ing_list.append('□')

    columns = len(header_ing)
    table = PrettyTable(header_ing)

    while ing_list:
        table.add_row(ing_list[:columns]) 
        # Используя срез переопределяем td_data так, чтобы он
        # больше не содержал первых 5 элементов.
        ing_list = ing_list[columns:]     
    shopping_list += (
        f'\n\n{str(table)}\n'
        f'\nИтого: {len(ingredients)} ингредиентов для {len(recipes)} рецептов.'
        f'\n\nПриятного аппетита!'       
        f'\n\nFoodgram ({today:%Y})'
        )
    filename = f'{user.username}_shopping_list.txt'
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response