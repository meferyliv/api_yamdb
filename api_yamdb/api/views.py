from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated

from reviews.models import Category, Genre, Title, User
from .permissions import IsRoleAdmin
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, AdminUserSerializer, SignupSerializer, TokenSerializer, UserSerializer
from reviews.uttils import send_confirmation_code
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, action
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsRoleAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsRoleAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsRoleAdmin)
    filter_backends = (SearchFilter,)
    filterset_fields = ('category', 'genre', 'name', 'year',)

#     def get_queryset(self):
#         queryset = self.queryset
#         if self.request.query_params.get('name'):
#             queryset = queryset.filter(
#                 name__icontains=self.request.query_params.get('name')
#             )
#         if self.request.query_params.get('category'):
#             queryset = queryset.filter(
#                 category__slug=self.request.query_params.get('category')
#             )
#         if self.request.query_params.get('genre'):
#             queryset = queryset.filter(
#                 genre__slug=self.request.query_params.get('genre')
#             )
#         return queryset

    def perform_create(self, serializer):
        category, genres = serializer.check_category_genre(
            self.request.data.get('category'),
            self.request.data.getlist('genre')
        )
        if category:
            serializer.save(category=category, genre=genres)
        else:
            serializer.save(genre=genres)

    def perform_update(self, serializer):
        category, genres = serializer.check_category_genre(
            self.request.data.get('category'),
            self.request.data.getlist('genre')
        )
        if category:
            serializer.save(category=category)
        title = get_object_or_404(Title, pk=self.kwargs.get('pk'))
        for genre in genres:
            title.genre.add(get_object_or_404(Genre, slug=genre))

            
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsRoleAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'
    search_fields = ('username',)

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def about_me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class UserRegView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class Token(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            return Response({'Wrong Code'}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)},
                        status=status.HTTP_200_OK)
