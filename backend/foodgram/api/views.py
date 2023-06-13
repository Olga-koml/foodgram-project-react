from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, permissions

from recipes.models import Ingredient, Recipe, Tag, FavoriteRecipe, ShoppingCart, RecipesIngredient
from users.models import Subscription
from .serializers import (IngredientSerializer, RecipeSerializer, 
                          TagSerializer, RecipePostSerializer, 
                          RecipeShortDescriptionSerializer, SubscriptionSerializer)

from django.core.exceptions import PermissionDenied

from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from .filters import IngredientFilter, RecipiesFilter
from api.mixins import GetListCreateDeleteMixin
from .serializers import SubscriptionSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework import status
from django.shortcuts import get_object_or_404
from .utilis import add_recipe_to, del_recipe_from, get_download_shopping_chart
from django.db.models import Sum
from django.shortcuts import HttpResponse
from datetime import datetime as dt
from django.contrib.auth import get_user_model
from .pagination import CustomPagination
from djoser.views import UserViewSet
#from users.views import CustomUserViewSet
from rest_framework.decorators import api_view

User = get_user_model()

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    #filter_backends = (DjangoFilterBackend, )
   
    filterset_class = IngredientFilter
    # filter_backends = (IngredientSearchField, )
    # search_fields = ('name',  )
    # filterset_class = IngredientFilter
   
    # def get_queryset(self):
    #     return Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete'] #проверить метод ПУТ
    filterset_class = RecipiesFilter
  
    
    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RecipePostSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        # if serializer.is_valid():
        #     serializer.save(author=self.request.user)
        serializer.save(author=self.request.user)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return add_recipe_to(RecipeShortDescriptionSerializer, FavoriteRecipe, request, pk)
        if request.method == 'DELETE':
            return del_recipe_from(FavoriteRecipe, request, pk)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return add_recipe_to(RecipeShortDescriptionSerializer, ShoppingCart, request, pk)
        if request.method == 'DELETE':
            return del_recipe_from(ShoppingCart, request, pk)
    
    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        return get_download_shopping_chart(request)

   
    # @decorators.action(
    #     detail=True,
    #     methods=['POST', 'DELETE'],
    #     permission_classes=[permissions.IsAuthenticated]
    # )
  

# class SubViewSet(GetListCreateDeleteMixin):
# # class SubscriptionViewSet(GetListCreateDeleteMixin):
# # class SubscriptionViewSet(viewsets.ModelViewSet): from djoser.views import UserViewSet
   
#     queryset = User.objects.all()
#     serializer_class = SubscriptionSerializer
#     pagination_class = CustomPagination
#     filter_backends = (SearchFilter,)
#     search_fields = ("fanatic__username", "idol__username")
    
#     # def list(self, request):
#     #     return Response({
#     #             'errors': 'ПРОВЕРКА АДРЕСА'
#     #             }, status=HTTP_400_BAD_REQUEST)
    
#     def subscriptions(self, request):
#         queryset = self.request.user.idol.all()
#         pagination = self.paginate_queryset(queryset)
#         serializer = SubscriptionSerializer(
#             pagination, many = True,
#             context={'request': request}
#         )
#         return self.get_paginated_response(serializer.data)
    
        # limit = self.kwargs.get('recipes_limit')
        # if limit is not None:
        #     return Subscription.objects.filter(fanatic=self.request.user)[:limit]
        # return Subscription.objects.filter(fanatic=self.request.user)

    # def perform_list(self, request):
    #     return Response({
    #             'errors': 'LKSDJFLSKDJFL'
    #             }, status=HTTP_400_BAD_REQUEST)
    
 

class SubscriptionViewSet(GetListCreateDeleteMixin):
# class SubscriptionViewSet(GetListCreateDeleteMixin):
# class SubscriptionViewSet(viewsets.ModelViewSet): from djoser.views import UserViewSet
   
    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer
    #pagination_class = CustomPagination
    # filter_backends = (SearchFilter,)
    # search_fields = ("fanatic__username", "idol__username")
    permission_classes = [IsAuthenticated]
    
    

    #@action(detail=False, url_path='subscriptions', permission_classes=[IsAuthenticated])
    # @api_view
    def subscriptions(self, request): 
          
        queryset = User.objects.filter(idol__fanatic=request.user)
        # print(queryset)
        # queryset = Subscription.objects.filter(fanatic= request.user)

        #queryset = self.request.user.fanatic.all()
        print(queryset, 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        # print(**queryset)
        pagination = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pagination, many = True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
    
    # def subscriptions(self, request):
    #     queryset = self.request.user.idol.all()
    #     pagination = self.paginate_queryset(queryset)
    #     serializer = SubscriptionSerializer(
    #         pagination, many = True,
    #         context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)
    # def perform_list(self, request):
    #     return Response({
    #             'errors': 'LKSDJFLSKDJFL'
    #             }, status=HTTP_400_BAD_REQUEST)
    # @action(methods='get', detail=False, url_path='subscriptions', 
    #         permission_classes=[IsAuthenticated])
    # def get_queryset(self, request):
        # limit = self.kwargs.get('recipes_limit')
        # if limit is not None:
        #     return Subscription.objects.filter(fanatic=self.request.user)[:limit]
        # return Subscription.objects.filter(fanatic=self.request.user)
    

#     #   @action(
#     #     detail=False,
#     #     permission_classes=[IsAuthenticated]
#     # )

#    def subscriptions(self, request):
        # queryset = self.request.user.idol.all()
        # pagination = self.paginate_queryset(queryset)
        # serializer = SubscriptionSerializer(
        #     pagination, many = True,
        #     context={'request': request}
        # )
        # return self.get_paginated_response(serializer.data)
#         return Response({
#                     'errors': 'LKSDJFLSKDJFL'
#                     }, status=HTTP_400_BAD_REQUEST)
#     #     current_user = request.user
    #     queryset = User.objects.filter(fanatic__user=current_user)
    #     paginated_queryset = self.paginate_queryset(queryset)
    #     serializer = SubscriptionSerializer(
    #         paginated_queryset,
    #         many=True,
    #         context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)
    # #  def get_filter_is_favorited(self, queryset, name, value):
    # #     user = self.request.user
    # #     if value and user.is_authenticated:
    # #         return queryset.filter(favorites__user=user)
    # #     return queryset
    # @action(methods=['get'], detail=False, 
    #         url_path='subscriptions', permission_classes=[IsAuthenticated])
    # def get_queryset(self):
    #    # return queryset.filter(fanatic__user=self.request.user)
    #     #print(obj, 'OBLKJLSKDJF')

    #     user = self.request.user
    #     queryset = Subscription.objects.filter(
    #                                           fanatic=user)
    #     return queryset
    #     # queryset = self.request.user.idol.all()
    #     # seri
        
    #     # return self.request.user.fanatic.all()
    # # def get_queryset(self):
    # #     user = get_object_or_404(User, username=self.request.user)
    # #     return Subscription.objects.filter(fanatic=user)  
    
    # # @action(detail=False, url_path='subscriptions', permission_classes=[IsAuthenticated])
    # # def get_queryset(self):
    # #     return self.request.user.fanatic



    @action(detail=True, methods=['post', 'delete'],
            url_path='subscribe', permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        idol = get_object_or_404(User, pk=pk)
        # idol_id = self.kwargs.get('id')
        print('USER строка 144', idol, 'request user - ', request.user)
        if request.method == "POST":
            if request.user.fanatic.filter(idol=idol).exists():
                return Response({
                    'errors': 'Вы уже подписаны на данного автора'
                    }, status=HTTP_400_BAD_REQUEST)
            elif request.user == idol:
                return Response({
                    'errors': 'Вы пытаетесь подписаться на самого себя'
                    }, status=HTTP_400_BAD_REQUEST)
            
            serializer = SubscriptionSerializer(
                idol, data=request.data,
                context={"request": request}
                )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(fanatic=request.user, idol=idol)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
      
        if request.method == "DELETE":
            if not Subscription.objects.filter(idol=idol, fanatic=request.user).exists():  
                return Response(
                    {'errors': 'Вы не были подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.objects.filter(idol=idol, fanatic=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        

    # @action(detail=False, methods=['get'], url_path='subscriptions',
    #         permission_classes=[IsAuthenticated])
    # @api_view(['GET'])
    # def get_queryset(self, request):
    # def list(self, request):
    #     return Response({
    #             'errors': 'LKSDJFLSKDJFL'
    #             }, status=HTTP_400_BAD_REQUEST)
    #def get_queryset(self, request):
        # limit = self.kwargs.get('recipes_limit')
        # if limit is not None:
        #     return Subscription.objects.filter(fanatic=self.request.user)[:limit]
        # return Subscription.objects.filter(fanatic=self.request.user)
    

    #   @action(
    #     detail=False,
    #     permission_classes=[IsAuthenticated]
    # )

    
        # queryset = self.request.user.idol.all()
        # pagination = self.paginate_queryset(queryset)
        # serializer = SubscriptionSerializer(
        #     pagination, many = True,
        #     context={'request': request}
        # )
        # return self.get_paginated_response(serializer.data)
   
    # #     current_user = request.user
    # #     queryset = User.objects.filter(fanatic__user=current_user)
    # #     paginated_queryset = self.paginate_queryset(queryset)
    # #     serializer = SubscriptionSerializer(
    # #         paginated_queryset,
    # #         many=True,
    # #         context={'request': request}
    # #     )
    # #     return self.get_paginated_response(serializer.data)
    # # #  def get_filter_is_favorited(self, queryset, name, value):
    # # #     user = self.request.user
    # # #     if value and user.is_authenticated:
    # # #         return queryset.filter(favorites__user=user)
    # # #     return queryset
    # # @action(methods=['get'], detail=False, 
    # #         url_path='subscriptions', permission_classes=[IsAuthenticated])
    # # def get_queryset(self):
    # #    # return queryset.filter(fanatic__user=self.request.user)
    # #     #print(obj, 'OBLKJLSKDJF')

    # #     user = self.request.user
    # #     queryset = Subscription.objects.filter(
    # #                                           fanatic=user)
    # #     return queryset
    # #     # queryset = self.request.user.idol.all()
    # #     # seri
        
    # #     # return self.request.user.fanatic.all()
    # # # def get_queryset(self):
    # # #     user = get_object_or_404(User, username=self.request.user)
    # # #     return Subscription.objects.filter(fanatic=user)  
    
    # # # @action(detail=False, url_path='subscriptions', permission_classes=[IsAuthenticated])
    # # # def get_queryset(self):
    # # #     return self.request.user.fanatic
