from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib


def homepage(request):
    # TODO: get genre from ttl static file
    ctx = {"genre": ["Action", "Romance", "Comedy"]}
    return render(request, 'homepage.html', ctx)


def actor_detail(request):
    data = {'name': 'Jenna Ortega'}
    return render(request, 'actor_detail.html', data)


def movie_search(request):
    data = {'movies': [{'title': 'Wednesday'}, {'title': 'Django Unchained'}]}

    return render(request, 'movie_search.html', data)


def movie_detail(request):
    data = {'title': 'Wednesday', 'Actors': [{'name': 'Jenna Ortega'}]}
    return render(request, 'movie_detail.html', data)
