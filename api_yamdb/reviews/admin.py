from django.contrib import admin
from .models import Category, Genre, Title, User
from api_yamdb.settings import EMPTY


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'rating',
        'description',
        'category',
    )
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = EMPTY


admin.site.register(User)
