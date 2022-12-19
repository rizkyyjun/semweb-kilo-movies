from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('movies/', views.movie_search, name='movie_search'),
    path('movies/<movie_id>', views.movie_detail, name='movie_detail'),
    path('actors/<actor_id>', views.actor_detail, name='actor_detail'),
]