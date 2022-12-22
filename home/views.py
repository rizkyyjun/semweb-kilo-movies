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
    title_filter = f"FILTER regex(lcase(?title), '{title.lower}') ." if title != "" else ""
    actor_filter = f"FILTER regex(lcase(?actorName), '{actor.lower}') ." if actor != "" else ""
    director_filter = f"FILTER regex(lcase(?directorName), '{director.lower}') ." if director != "" else ""
    genre_filter = f"FILTER regex(lcase(?genreLabel), '{genre.lower}') ." if genre != "" else ""

    yearAfter = yearAfter if yearAfter != "" else 0
    yearBefore = yearBefore if yearBefore != "" else 10000
    year_filter = f"FILTER (?year >= {yearAfter}^^xsd:gYear && ?year <= {yearBefore}^^xsd:gYear ) ."

    ratingMoreThan = ratingMoreThan if ratingMoreThan != "" else 0.0
    ratingLessThan = ratingLessThan if ratingLessThan != "" else 10000.0
    rating_filter = f"FILTER (?rating >= '{ratingMoreThan}'^^xsd:double && ?rating <= '{ratingLessThan}'^^xsd:double )."

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
      
      %s
      %s
      %s
      %s
      %s
      %s
         
    } GROUP BY ?movie ?title ?directorName ?desc ?rating ?year ?runtime ?votes ?rank ?revenue
        """ % (title_filter, actor_filter, director_filter, genre_filter, rating_filter,year_filter)
    # TODO: Implement filter by year

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

    ctx = {'movies': movie_search_query(title, actor, director, genre, yearAfter, yearBefore, ratingMoreThan,
                                        ratingLessThan), 'genre': genre_query()}

    # print(ctx)
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

def actor_detail_query(actor_name):
    actor_name = f'dbp:{actor_name}'
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

def movie_search(request):
    data = {'movies': [{'title': 'Wednesday'}, {'title': 'Django Unchained'}]}

    return render(request, 'movie_search.html', data)
