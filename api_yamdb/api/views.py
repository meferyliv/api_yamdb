from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Title
from .permissions import IsRoleAdmin
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


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

    # def get_queryset(self):
    #     queryset = self.queryset
    #     if self.request.query_params.get('name'):
    #         queryset = queryset.filter(
    #             name__icontains=self.request.query_params.get('name')
    #         )
    #     if self.request.query_params.get('category'):
    #         queryset = queryset.filter(
    #             category__slug=self.request.query_params.get('category')
    #         )
    #     if self.request.query_params.get('genre'):
    #         queryset = queryset.filter(
    #             genre__slug=self.request.query_params.get('genre')
    #         )
    #     return queryset

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
