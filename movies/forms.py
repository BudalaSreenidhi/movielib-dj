from django import forms
from .models import MovieList, Movie
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class MovieListForm(forms.ModelForm):
    class Meta:
        model = MovieList
        fields = ['name', 'is_public']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title'] 
        