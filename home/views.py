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


def movie_detail_query(movie_id):
    query = """
    SELECT ?movie ?title ?desc ?directorName ?rating (GROUP_CONCAT(distinct(?genreLabel);SEPARATOR=", ") AS ?genres) (GROUP_CONCAT(distinct(?actor);SEPARATOR=", ") AS ?actorsIRI) (GROUP_CONCAT(distinct(?actorName);SEPARATOR=", ") AS ?actorNames)  ?year ?runtime ?votes ?rank ?revenue
    WHERE {
        ?movie rdf:type :Movie .
        OPTIONAL {{?movie :actors ?actor .
                  ?actor rdfs:label ?actorName . }}
        OPTIONAL {{?movie :director ?director. 
                  ?director rdfs:label ?directorName .}}
        OPTIONAL {{?movie :genre ?genre .
                  ?genre rdfs:label ?genreLabel .}}
        OPTIONAL {{?movie :description ?desc .}}
        OPTIONAL {{?movie :metascore ?metascore .}}
        OPTIONAL {{?movie :rank ?rank .}}
        OPTIONAL {{?movie :rating ?rating .}}
        OPTIONAL {{?movie :revenue ?revenue .}}
        OPTIONAL {{?movie :runtime ?runtime .}}
        OPTIONAL {{?movie :votes ?votes .}}
        OPTIONAL {{?movie :title ?title .}}
        OPTIONAL {{?movie :year ?year .}}
      FILTER regex(str(?movie), "%s$")
    } GROUP BY ?movie ?title ?directorName ?desc ?rating ?year ?runtime ?votes ?rank ?revenue
    """ % movie_id

    g = rdflib.Graph()
    g.parse('home/static/movies.ttl')
    try:
        res = g.query(query)
        res = process_result(res)

        return res
    except Exception:
        return "error"


def process_result(result):
    res = {}

    for row in result:
        actors = []
        for key, value in dict(zip(row.actorsIRI.toPython().split(', '), row.actorNames.toPython().split(', '))).items():
            actors.append({'id': key, 'name': value})

        temp = {
            'id': row.movie.toPython(),  # ini harusnya gaada
            'title': row.title.toPython(),
            'description': row.desc.toPython(),
            'director': row.directorName.toPython(),
            'rating': row.rating.toPython(),
            'genre': row.genres.toPython(),
            'actors': actors,
            'year': row.year.toPython(),
            'runtime': row.runtime.toPython(),
            'votes': row.votes.toPython(),
            'rank': row.rank.toPython(),
            'revenue': row.revenue.toPython()
        }
        res = temp

    return res


def movie_detail(request, movie_id):
    ctx = movie_detail_query(movie_id)
    return render(request, 'movie_detail.html', ctx)


def actor_detail(request):
    data = {'name': 'Jenna Ortega'}
    return render(request, 'actor_detail.html', data)


def movie_search(request):
    data = {'movies': [{'title': 'Wednesday'}, {'title': 'Django Unchained'}]}

    return render(request, 'movie_search.html', data)


def movie_detail(request):
    data = {'title': 'Wednesday', 'Actors': [{'name': 'Jenna Ortega'}]}
    return render(request, 'movie_detail.html', data)
