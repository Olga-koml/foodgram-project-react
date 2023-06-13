from django.contrib import admin

# Register your models here.
from .models import Ingredient, Recipe, Tag, RecipesIngredient

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class RecipesIngredientInLine(admin.StackedInline):
    #list_display = ('recipe', 'ingredient', 'amount',)
    model = RecipesIngredient
    extra = 2
    autocomplete_fields = ('ingredient',)
    

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipesIngredientInLine,)
    list_display = ('name', 'id', 'author', ) #'added_in_favorites'
    #readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name', 'tags',)

    # @display(description='Количество в избранных')
    # def added_in_favorites(self, obj):
    #     return obj.favorites.count()
    
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'name',
#         'year',
#         'category',
#         'description'
#     )
    # list_editable = ('name', 'year', 'description')
    # search_fields = ('name', 'year', 'category', 'genre')
    # list_filter = ('name', 'year', 'category', 'genre')
    # empty_value_display = '-пусто-'


