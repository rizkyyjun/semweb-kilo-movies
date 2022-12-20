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


def movie_detail_query(movie_name):
    movie_name = movie_name.lower()
    query = """
    SELECT ?movie ?title ?desc ?directorName ?rating (GROUP_CONCAT(distinct(?genreLabel);SEPARATOR=", ") AS ?genres) (GROUP_CONCAT(distinct(?actorName);SEPARATOR=", ") AS ?actorNames) ?year ?runtime ?votes ?rank ?revenue
    WHERE {
        ?movie rdf:type :Movie .
        OPTIONAL {{?movie :actors ?actor ;}}
        OPTIONAL {{?movie :director ?director;}}
        OPTIONAL {{?movie :genre ?genre ;}}
        OPTIONAL {{?movie :description ?desc ;}}
        OPTIONAL {{?movie :metascore ?metascore ;}}
        OPTIONAL {{?movie :rank ?rank ;}}
        OPTIONAL {{?movie :rating ?rating ;}}
        OPTIONAL {{?movie :revenue ?revenue ;}}
        OPTIONAL {{?movie :runtime ?runtime ;}}
        OPTIONAL {{?movie :votes ?votes ;}}
        OPTIONAL {{?movie :title ?title ;}}
        OPTIONAL {{?movie :year ?year .}}
      ?director rdfs:label ?directorName .
      ?actor rdfs:label ?actorName .
      ?genre rdfs:label ?genreLabel .
      FILTER regex(lcase(?title), '%s')
    } GROUP BY ?movie ?title ?directorName ?desc ?rating ?year ?runtime ?votes ?rank ?revenue
    """ % movie_name

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
        temp = {
            'id': 1,  # ini harusnya gaada
            'title': row.title.toPython(),
            'description': row.desc.toPython(),
            'director': row.directorName.toPython(),
            'rating': row.rating.toPython(),
            'genre': row.genres.toPython(),
            'actors': row.actorNames.toPython().split(', '),
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
    print(ctx)
    return render(request, 'movie_detail.html', ctx)


def actor_detail(request):
    data = {'name': 'Jenna Ortega'}
    return render(request, 'actor_detail.html', data)

def actor_detail_query(input):
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')
    query = '''
    SELECT *
    WHERE {
        ?film dbo:starring ?actor .
        ?actor dbo:abstract ?abstract;
            dbo:birthDate ?birthDate;
            dbp:name ?name;
            dbp:nationality ?nationality.
        FILTER (lang(?abstract) = "en" && lang(?name) = "en" && lang(?nationality) = "en")
    }
    LIMIT 1
    '''

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        qres = sparql.query().convert()
        for res in qres['results']['bindings']:
            print(res)
            break
        return qres
    except Exception:
        return "SPARQL Error!"
