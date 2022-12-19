from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib


def index(request):
    data = {'genres': ['action', 'romance', 'comedy']}  # stubs, TODO: query from ttl to get list of genre
    return render(request, 'home.html', data)


def actor_detail(request):
    data = {'name': 'Jenna Ortega'}
    return render(request, 'actor_detail.html', data)


def movie_search(request):
    data = {'movies': [{'title': 'Wednesday'}, {'title': 'Django Unchained'}]}

    return render(request, 'movie_search.html', data)


def movie_detail(request):
    data = {'title': 'Wednesday', 'Actors': [{'name': 'Jenna Ortega'}]}
    return render(request, 'movie_detail.html', data)
