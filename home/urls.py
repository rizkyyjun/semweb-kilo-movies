from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movie_search, name='movie_search'),
    path('movies/<movie_name>', views.movie_detail, name='movie_detail'),
    path('actors/<actor_name>', views.actor_detail, name='actor_detail'),
]