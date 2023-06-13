from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, SubscriptionViewSet
from . import views

app_name = 'api'

router = DefaultRouter()
# router.register(r'subscriptions', SubViewSet)
# router.register(r'users/subscriptions', SubscriptionViewSet)
router.register(r'users', SubscriptionViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet)


urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'subscriptions'})),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    
    
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('v1/auth/', include([
    #     path('token/', create_token),
    #     path('signup/', create_user)
    # ]))
]

# router.register(r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet, basename='reviews'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet, basename='comments'