from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import MovieForm
from .models import Movie

def home(request):
    return render(request, "movies/home.html")  # Corregido

def list_movies(request):
    movies = Movie.objects.filter(user=request.user)
    return render(request, "movies/movies.html", {"movies": movies})  # Corregido

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    return render(request, "movies/movie_detail.html", {"movie": movie})  # Corregido

def create_movie(request):
    if request.method == "GET":
        return render(request, 'movies/create_movie.html', {'form': MovieForm()})  # Corregido
    else:
        try:
            form = MovieForm(request.POST)
            new_movie = form.save(commit=False)
            new_movie.user = request.user
            new_movie.save()
            return redirect("list_movies")
        except ValueError:
            return render(request, 'movies/create_movie.html', {'form': MovieForm(), 'error': 'Datos inválidos'})  # Corregido

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    if request.method == "GET":
        form = MovieForm(instance=movie)
        return render(request, "movies/edit_movie.html", {"movie": movie, "form": form})  # Corregido
    else:
        try:
            form = MovieForm(request.POST, instance=movie)
            form.save()
            return redirect("list_movies")
        except ValueError:
            return render(request, "movies/edit_movie.html", {"movie": movie, "form": form, "error": "Error al actualizar"})  # Corregido

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, user=request.user)
    if request.method == "POST":
        movie.delete()
        return redirect("list_movies")
    return render(request, "movies/delete_movie.html", {"movie": movie})  # Corregido

def signup(request):
    if request.method == "GET":
        return render(request, "movies/signup.html", {"form": UserCreationForm()})  # Corregido
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("list_movies")
            except IntegrityError:
                return render(request, "movies/signup.html", {"form": UserCreationForm(), "error": "Usuario ya existe"})  # Corregido
        else:
            return render(request, "movies/signup.html", {"form": UserCreationForm(), "error": "Contraseñas no coinciden"})  # Corregido

def signin(request):
    if request.method == "GET":
        return render(request, "movies/signin.html", {"form": AuthenticationForm()})  # Corregido
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "movies/signin.html", {"form": AuthenticationForm(), "error": "Usuario/contraseña incorrectos"})  # Corregido
        else:
            login(request, user)
            return redirect("list_movies")

def signout(request):
    logout(request)
    return redirect("home")