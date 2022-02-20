from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import CategoryViewSet, GenreViewSet, UsersViewSet, UserRegView, Token, TitleViewSet


router = SimpleRouter()
router.register('users', UsersViewSet)
router_part_B_v1 = DefaultRouter()
router_part_B_v1.register(r'categories', CategoryViewSet, basename='category')
router_part_B_v1.register(r'genres', GenreViewSet, basename='genre')
router_part_B_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(router_part_B_v1.urls)),
    path('v1/auth/signup/', UserRegView.as_view()),
    path('v1/auth/token/', Token.as_view()),
]
