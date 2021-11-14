from django.shortcuts import redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import ReviewForm
from .models import Movie, Actor


class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'


class AddReview(View):

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_path())


class ActorView(DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'