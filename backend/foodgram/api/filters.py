from rest_framework.filters import SearchFilter
from recipes.models import Ingredient, Recipe, Tag
from django_filters.rest_framework import FilterSet, filters
# from django_filters.filters import OrderingFilter

# class IngredientSearchField(SearchFilter):
#     search_param = 'name'



class IngredientFilter(FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
        )

    class Meta:
        model = Ingredient
        fields = ('name', )
        # fields = {
        #     "name": ["istartswith", "icontains"],
        # }

# class IngredientFilter(FilterSet):
#     name = filters.CharFilter(
#         field_name='name',
#         lookup_expr='istartswith'
#         )
#     name_icontains = filters.CharFilter(
#         field_name='name',
#         #lookup_expr='istartswith'
#         lookup_expr='icontains')
    
#     order_by_field = 'ordering'
#     ordering = OrderingFilter(
#         # fields(('model field name', 'parameter name'),)
#         fields=(
#             ('name', 'name'),
#             ('name', 'name_icontains'),
#         )
#     )

#     class Meta:
#         model = Ingredient
#         fields = ('name', 'name_icontains')


class RecipiesFilter(FilterSet):
   
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name="slug",  
    )
    is_favorited = filters.BooleanFilter(method='get_filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='get_filter_is_in_shopping_cart')

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
    
  
