from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Ingredient, Recipe, RecipesIngredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class RecipesIngredientInLine(admin.StackedInline):
    model = RecipesIngredient
    extra = 2
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipesIngredientInLine,)
    list_display = (
        'name', 'id', 'author',
        'get_count_favorites', 'get_mini_picture'
    )
    readonly_fields = ('get_count_favorites',)
    list_filter = ('author', 'name', 'tags',)
    save_on_top = True

    @admin.display(description='Добавлен в избранное')
    def get_count_favorites(self, obj):
        return obj.favorites.count()

    @admin.display(description='Фото')
    def get_mini_picture(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")
