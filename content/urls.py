from django.urls import path
from content import views

urlpatterns = [
    path('', views.show_base, name='base'),
]