from django.urls import path
from . import views

urlpatterns = [
    path('album/', views.album_view, name='album'),
    path('collections/', views.collections_view, name='collections'),
]