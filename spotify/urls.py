from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('search/', views.search_song, name='search'),
    path('<str:username>/', views.recommend_song, name='recommend_song'),
    # path('collections/<str:username>/', views.recommend_songs, name='collections'),

]
