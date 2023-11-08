from django.urls import path
from . import views

urlpatterns = [
    path('album/', views.album_view, name='album'),
    path('select_genres/', views.select_genres, name='select_genres'),
]