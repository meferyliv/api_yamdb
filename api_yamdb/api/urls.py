from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import UsersViewSet, UserRegView, Token

router = SimpleRouter()
router.register('users', UsersViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserRegView.as_view()),
    path('v1/auth/token/', Token.as_view()),
]
