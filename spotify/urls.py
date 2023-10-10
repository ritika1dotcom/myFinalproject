from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('search/', views.search_song, name='search'),
]
