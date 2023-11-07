from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('search/', views.search_song, name='search'),
    path('fetch-songs/', views.fetch_and_save_songs, name='fetch_songs'),
    path('discover-associations/', views.discover_song_associations, name='discover_associations'),
]
