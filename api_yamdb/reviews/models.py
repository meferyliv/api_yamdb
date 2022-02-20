from django.db import models


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(
        'Адрес в URL - category/', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name[:20]


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField(
        'Адрес в URL - genres/', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-name',)

    def __str__(self):
        return self.name[:20]


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=100)
    year = models.IntegerField('Дата выхода произведения')
    rating = models.IntegerField('Рейтинг', null=True)
    description = models.CharField(
        'Описание произведения', max_length=1000, null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-name',)

    def __str__(self):
        return self.name[:20]
