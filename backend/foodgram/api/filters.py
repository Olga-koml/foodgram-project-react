from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    """Класс для фильтрации ингредиентов ио имени."""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
        )

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipiesFilter(FilterSet):
    """Класс для фильтрации рецептов по тегам, избранным и корзине покупок"""

    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name="slug",
    )
    is_favorited = filters.BooleanFilter(method='get_filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_filter_is_in_shopping_cart'
        )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping__user=user)
        return queryset
