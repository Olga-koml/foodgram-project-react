from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, SubscriptionViewSet,
                    TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', SubscriptionViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view(
        {'get': 'subscriptions'}
        )),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
