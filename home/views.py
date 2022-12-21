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
    ctx = {"genre": genre_query()}
    return render(request, 'homepage.html', ctx)


def movie_search_query(title, actor, director, genre, yearAfter, yearBefore, ratingMoreThan, ratingLessThan):
    query = """
        SELECT ?movie ?title ?directorName ?rating (GROUP_CONCAT(distinct(?genreLabel);SEPARATOR=", ") AS ?genres) ?year
    WHERE {
      ?movie rdf:type :Movie .
      OPTIONAL {{?movie :director ?director. 
                 ?director rdfs:label ?directorName .}}
      OPTIONAL {{?movie :actors ?actor .
                 ?actor rdfs:label ?actorName . }}
      OPTIONAL {{?movie :genre ?genre .
                 ?genre rdfs:label ?genreLabel .}}
      OPTIONAL {{?movie :rating ?rating .}}
      OPTIONAL {{?movie :title ?title .}}
      OPTIONAL {{?movie :year ?year .}}
      
      FILTER regex(lcase(?title), "%s") .
      FILTER regex(lcase(?actorName), "%s") .
      FILTER regex(lcase(?directorName), "%s") .
      FILTER regex(lcase(?genreLabel), "%s") .
      
      FILTER (?rating >= "%s"^^xsd:double && ?rating <= "%s"^^xsd:double ).
             
    } GROUP BY ?movie ?title ?directorName ?desc ?rating ?year ?runtime ?votes ?rank ?revenue
        """ % (title.lower(), actor.lower(), director.lower(), genre.lower(), float(ratingMoreThan), float(ratingLessThan))
    # TODO: Implement filter by year and rating

    print(query)

    g = rdflib.Graph()
    g.parse('home/static/movies.ttl')
    try:
        res = g.query(query)
        res = process_result(res, "movie_search")

        return res
    except Exception:
        return "error"


def genre_query():
    query = """
    SELECT (GROUP_CONCAT(distinct(?genreLabel);SEPARATOR=", ") AS ?genres)
    WHERE {
      ?genre rdf:type :Genre ;
             rdfs:label ?genreLabel .
    }
    """
    g = rdflib.Graph()
    g.parse('home/static/movies.ttl')
    try:
        res = g.query(query)
        res = process_result(res, "genre")

        return res
    except Exception:
        return "error"


def movie_search(request):
    title = request.GET.get('title')
    actor = request.GET.get('actor')
    director = request.GET.get('director')
    genre = request.GET.get('genre')
    yearAfter = request.GET.get('yearAfter')
    yearBefore = request.GET.get('yearBefore')
    ratingMoreThan = request.GET.get('ratingMoreThan')
    ratingLessThan = request.GET.get('ratingLessThan')

    # TODO: get movies and genre from backend function
    # ctx = {'movies': [
    #     {'id': 2, 'title': 'Wednesday', 'director': 'Christopher Nolan', 'rating': 4.8, 'genre': 'Thriller'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    #     {'id': 1, 'title': 'Django Unchained', 'director': 'Sule Sutrisna', 'rating': 2.4, 'genre': 'Comedy'},
    # ]}
    ctx = {'movies': movie_search_query(title, actor, director, genre, yearAfter, yearBefore, ratingMoreThan,
                                        ratingLessThan), 'genre': genre_query()}

    print(ctx)
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
        res = process_result(res, "movie_detail")

        return res
    except Exception:
        return "error"


def process_result(result, query_type):
    res = []
    for row in result:
        if query_type == "movie_detail":
            actors = []
            for key, value in dict(
                    zip(row.actorsIRI.toPython().split(', '), row.actorNames.toPython().split(', '))).items():
                actors.append({'id': key, 'name': value})

            temp = {
                'id': row.movie.toPython(),
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
            return temp
        elif query_type == "movie_search":
            temp = {
                'id': row.movie.toPython(),
                'title': row.title.toPython(),
                'director': row.directorName.toPython(),
                'rating': row.rating.toPython(),
                'genre': row.genres.toPython(),
            }
            res.append(temp)
        elif query_type == "genre":
            return row.genres.toPython().split(", ")

    return res


def movie_detail(request, movie_id):
    ctx = movie_detail_query(movie_id)
    return render(request, 'movie_detail.html', ctx)


def actor_detail(request):
    data = {'name': 'Jenna Ortega'}
    return render(request, 'actor_detail.html', data)
