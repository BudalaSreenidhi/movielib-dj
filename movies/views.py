import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MovieList, Movie
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import MovieListForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm

def logout(request):
    return render(request,'registration/logout.html')

@login_required
def home(request):
    user_lists = MovieList.objects.filter(user=request.user)
    public_lists = MovieList.objects.filter(is_public=True).exclude(user=request.user)
    return render(request, 'movies/home.html', {'user_lists': user_lists, 'public_lists': public_lists})


@login_required
def my_lists(request):
    user_lists = MovieList.objects.filter(user=request.user)
    public_lists = MovieList.objects.filter(is_public=True).exclude(user=request.user)
    return render(request, 'movies/my_lists.html', {'user_lists': user_lists, 'public_lists': public_lists})

def view_list(request, list_id):
    movie_list = MovieList.objects.get(id=list_id)
    return render(request, 'movies/view_list.html', {'list': movie_list})


@login_required
def create_list(request):
    if request.method == 'POST':
        list_form = MovieListForm(request.POST)
        if list_form.is_valid():
            movie_list = list_form.save(commit=False)
            movie_list.user = request.user
            movie_list.save()
            return redirect('add_to_list', list_id=movie_list.id)
    else:
        list_form = MovieListForm()
    return render(request, 'movies/create_list.html', {'list_form': list_form})

@login_required
def add_to_list(request, list_id):
    movie_list = MovieList.objects.get(id=list_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        # Fetch movies from OMDB API based on the title
        search_url = f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={title}'
        response = requests.get(search_url)
        data = response.json()
        movies = data.get('Search', [])
        return render(request, 'movies/add_to_list.html', {'movie_list': movie_list, 'movies': movies})
    return render(request, 'movies/add_to_list.html', {'movie_list': movie_list})

from django.urls import reverse

@login_required
def select_movies(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id)
    if request.method == 'POST':
        movie_ids = request.POST.getlist('movie_id')
        for movie_id in movie_ids:
            # Fetch movie details from OMDB API based on movie ID
            movie_url = f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&i={movie_id}'
            response = requests.get(movie_url)
            data = response.json()
            # Create a new movie object and add it to the list
            movie, created = Movie.objects.get_or_create(
                imdb_id=data.get('imdbID'),
                defaults={
                    'title': data.get('Title'),
                    'year': data.get('Year'),
                    'poster': data.get('Poster')
                }
            )
            movie_list.movies.add(movie)
        # Redirect to the view_list page for the specific list_id
        return redirect('view_list', list_id=list_id)
    # Redirect to the home page if it's not a POST request
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/signin.html', {'form': form})

def my_lists(request):
    lists = MovieList.objects.filter(user=request.user)
    return render(request, 'movies/my_lists.html', {'lists': lists})

def search_movies(request):
    query = request.GET.get('q')
    if query:
        search_url = f'http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={query}'
        search_response = requests.get(search_url)
        search_data = search_response.json()
        movies = search_data.get('Search', [])
    else:
        movies = []
    return render(request, 'movies/search.html', {'movies': movies})

def delete_list(request, list_id):
    # Get the playlist object
    playlist = get_object_or_404(MovieList, id=list_id)
    
    # Check if the request method is POST
    if request.method == 'POST':
        # Check if the playlist belongs to the current user
        if playlist.user == request.user:
            # Delete the playlist
            playlist.delete()
            # Redirect to the home page
            return redirect('my_lists')
        else:
            # If the playlist does not belong to the current user, display an error message
            messages.error(request, "You don't have permission to delete this list.")
            # Redirect the user to a different page, or handle the error as per your application's design
            return redirect('home')  # Redirect to the home page or another page
    # If the request method is not POST, maybe show a confirmation page?
    return render(request, 'confirmation_template.html', {'playlist': playlist})

def delete_movies(request, list_id):
    if request.method == 'POST':
        movie_ids = request.POST.getlist('movie_ids')
        movie_list = get_object_or_404(MovieList, id=list_id)
        movie_list.movies.filter(id__in=movie_ids).delete()
    return redirect('view_list', list_id=list_id)

@login_required
def get_public_lists(request):
    public_lists = MovieList.objects.filter(is_public=True).select_related('user').prefetch_related('movies')
    return render(request, 'movies/public_lists.html', {'public_lists': public_lists})

@login_required
def copy_list(request):
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        public_list = get_object_or_404(MovieList, id=list_id)
        user_list = MovieList.objects.create(user=request.user, name=f"{public_list.name}", is_public=False)
        for movie in public_list.movies.all():
            user_list.movies.add(movie)
        return redirect('my_lists')
    return redirect('home')