from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_pets, name='list_pets'),
    path('request_adoption/<int:pet_id>', views.request_adoption, name="request_adoption"), # noqa E501
]
