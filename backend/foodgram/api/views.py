from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Tag)
from users.models import Subscription
from .filters import IngredientFilter, RecipiesFilter
from .mixins import GetListCreateDeleteMixin
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipePostSerializer,
                          RecipeSerializer, RecipeShortDescriptionSerializer,
                          SubscriptionSerializer, TagSerializer)
from .utilis import add_recipe_to, del_recipe_from, get_download_shopping_chart

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для игредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = RecipiesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RecipePostSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return add_recipe_to(
                RecipeShortDescriptionSerializer, FavoriteRecipe, request, pk
            )
        if request.method == 'DELETE':
            return del_recipe_from(FavoriteRecipe, request, pk)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return add_recipe_to(
                RecipeShortDescriptionSerializer, ShoppingCart, request, pk
            )
        if request.method == 'DELETE':
            return del_recipe_from(ShoppingCart, request, pk)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        return get_download_shopping_chart(request)


class SubscriptionViewSet(GetListCreateDeleteMixin):
    """Вьюсет для подписки/отписки на автора рецептов,
    для отображения всех подписок пользователя"""

    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        pagination = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pagination, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            url_path='subscribe', permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        if request.method == "POST":
            if request.user.subscriber.filter(author=author).exists():
                return Response({
                    'errors': 'Вы уже подписаны на данного автора'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif request.user == author:
                return Response({
                    'errors': 'Вы пытаетесь подписаться на самого себя'
                    }, status=status.HTTP_400_BAD_REQUEST)
            serializer = SubscriptionSerializer(
                author, data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            if not Subscription.objects.filter(
                author=author, user=request.user
                                               ).exists():
                return Response(
                    {'errors': 'Вы не были подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.objects.filter(
                author=author, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
