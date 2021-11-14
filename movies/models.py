from datetime import date

from django.db import models


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=150)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100)
    age = models.PositiveIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'актеры и режиссеры'


class Genre(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=150)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    tag_line = models.CharField(verbose_name='Слоган', max_length=100, default='')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(verbose_name='Постер', upload_to='movies/')
    year = models.PositiveIntegerField(verbose_name='Год выхода', default=2019)
    country = models.CharField(verbose_name='Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField(verbose_name='Примьера в мире', default=date.today)
    budget = models.PositiveIntegerField(verbose_name='Бюджет', default=0, help_text='указывать сумму в долларах')
    fess_in_usa = models.PositiveIntegerField(verbose_name='Сборы в США', default=0,
                                              help_text='указывать сумму в долларах')
    fess_in_world = models.PositiveIntegerField(verbose_name='Сборы в мире', default=0,
                                                help_text='указывать сумму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_path(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='actors/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    value = models.PositiveIntegerField(verbose_name='Значение', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'


class Rating(models.Model):
    ip = models.CharField(verbose_name='IP адресс', max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name='Звезда', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.star, self.movie)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField(verbose_name='Имя', max_length=100)
    text = models.TextField(verbose_name='Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.movie)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
