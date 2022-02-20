from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def check_category_genre(self, category, genre):
        if category:
            existing_category = Category.objects.filter(slug=category)
            if not existing_category:
                raise serializers.ValidationError(
                    f'{category} category does not exist'
                )
        else:
            existing_category = None
        existing_genres = []
        list_genres = genre
        for genre_slug in list_genres:
            existing_genre = Genre.objects.filter(slug=genre_slug)
            if existing_genre:
                existing_genres.append(
                    get_object_or_404(Genre, slug=genre_slug)
                )
            else:
                raise serializers.ValidationError(
                    f'{genre_slug} genre does not exist')
        return existing_category, existing_genres
