from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router_part_B_v1 = DefaultRouter()
router_part_B_v1.register(r'categories', CategoryViewSet, basename='category')
router_part_B_v1.register(r'genres', GenreViewSet, basename='genre')
router_part_B_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_part_B_v1.urls)),
]
