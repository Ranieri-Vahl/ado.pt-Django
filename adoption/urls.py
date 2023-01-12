from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_pets, name='list_pets')
]
