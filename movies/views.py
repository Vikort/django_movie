from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Movie


class MoviesView(ListView):

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):

    model = Movie
    slug_field = 'url'
