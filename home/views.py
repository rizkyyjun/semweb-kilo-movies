from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib
import urllib.parse


def homepage(request):
    if request.GET:
        url = "/movies/?" + urllib.parse.urlencode(request.GET) + "#search-result"
        return HttpResponseRedirect(url)

    # TODO: get genre from backend function
    ctx = {"genre": ["Action", "Romance", "Comedy"]}
    return render(request, 'homepage.html', ctx)


def movie_search(request):
    # TODO: get movies and genre from backend function
    ctx = {'movies': [
        {'id': 2, 'title': 'Wednesday', 'director': 'Christopher Nolan', 'rating': 4.8, 'genre': 'Thriller'}, 
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
        {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    ]}
    ctx['genre'] = ["Action", "Romance", "Comedy"]

    return render(request, 'movie_search.html', ctx)


def movie_detail(request):
    data = {'title': 'Wednesday', 'Actors': [{'name': 'Jenna Ortega'}]}
    return render(request, 'movie_detail.html', data)


def actor_detail(request):
    data = {'name': 'Jenna Ortega'}
    return render(request, 'actor_detail.html', data)
