from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib

def index(request):
    data = {'genres': ['action', 'romance', 'comedy']} # stubs, TODO: query from ttl to get list of genre
    return render(request, 'home.html', data)