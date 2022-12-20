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


def movie_detail(request, movie_id):
    # TODO: get detail from backend function
    ctx = {
        'id': 2, 
        'title': 'Wednesday', 
        'description': 'Hari Rabu',
        'director': 'Christopher Nolan', 
        'rating': 4.8, 
        'genre': 'Thriller',
        'actors': [{'id': 1, 'name': 'Sule'}, {'id': 2, 'name': 'Andre'}],
        'year': 2021,
        'runtime': 201,
        'votes': 12,
        'rank': 2,
        'revenue': 128
    }
    if movie_id == "1":
        ctx = {
            'id': 1, 
            'title': 'wot u doin step brother', 
            'description': 'Stuck in washing machine',
            'director': 'Pronbuh', 
            'rating': 9.9, 
            'genre': 'Family',
            'actors': [{'id': 3, 'name': 'Sis'}, {'id': 4, 'name': 'Bro'}],
            'year': 2077,
            'runtime': 15,
            'votes': 51534,
            'rank': 1,
            'revenue': 696969
        }
    return render(request, 'movie_detail.html', ctx)


def actor_detail(request):
    data = {'name': 'Jenna Ortega'}
    return render(request, 'actor_detail.html', data)

def dbpedia_query(input):
    query = """
        SELECT ?title ?wiki (group_concat(distinct ?cast;separator=", ") as ?casts) (group_concat(distinct ?castName;separator=", ") as ?castsName) (group_concat(distinct ?director;separator=", ") as ?directors) (group_concat(distinct ?directorName;separator=", ") as ?directorsName)  (group_concat(distinct ?producer;separator=", ") as ?producers) (group_concat(distinct ?producerName;separator=", ") as ?producersName) (group_concat(distinct ?writer;separator=", ") as ?writers)  (group_concat(distinct ?writerName;separator=", ") as ?writersName) (group_concat(distinct ?genre;separator=", ") as ?genres) ?country ?runtime ?desc ?release WHERE
            {{
                ?film rdfs:label ?title ;
                    dbo:starring ?cast ;
                    rdf:type ?category ;
                    dbp:country ?country ;
                    dbo:Work\/runtime ?runtime ;
                    dbo:abstract ?desc ;
                    owl:sameAs ?wiki ;
                    dbo:distributor [ dbo:parentCompany ?distributor ] .
                ?cast rdfs:label ?castName .
                {}
                OPTIONAL {{ ?film dbo:director ?director .
                                    ?director foaf:name ?directorName .
                                    FILTER (lang(?directorName) = "en") }}
                OPTIONAL {{ ?film dbo:producer ?producer .
                                    ?producer foaf:name ?producerName .
                                    FILTER (lang(?producerName) = "en") }}
                OPTIONAL {{ ?film dbo:writer ?writer.
                                    ?writer foaf:name ?writerName .
                                    FILTER (lang(?writerName) = "en") }}
                OPTIONAL {{ ?film dbp:released ?release }}
                OPTIONAL {{ ?film dbp:genre ?genre }}
                FILTER (regex(str(?wiki), "wikidata") && lang(?title) = "en" && lang(?desc) = "en" && lang(?castName) = "en" && regex(str(?distributor), "Disney") {})
            }}
        GROUP BY ?title ?wiki ?country ?runtime ?desc ?release 

    """.format('?film a dbo:Film' if input[0] == 'film' else '?film a dbo:TelevisionShow' if input[0] == 'tv show' else subquery(input), input[1] if input[0] == 'film' or input[0] == 'tv show' else '')

    # print(query)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        res = sparql.query().convert()
        for movie in res['results']['bindings']:
            # print(movie)
            break
        return res
    except Exception:
        return "SPARQL Error!"
