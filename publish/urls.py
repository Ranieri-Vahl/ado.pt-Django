from django.urls import path

from . import views

urlpatterns = [
    path('new_pet/', views.new_pet, name='new_pet'),
    path('new_pet/create', views.new_pet_create, name='new_pet_create'),
    path('your_pets/', views.your_pets, name='your_pets'),
    path('remove_pet/<int:id_remove>', views.remove_pet, name='remove_pet'),
    path('see_pet/<int:id>', views.see_pet, name='see_pet'), 
    path('see_request_adoption/', views.see_request_adoption, name='see_request_adoption'),   # noqa E501
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api_adoptions_by_breed/', views.api_adoptions_by_breed, name='api_adoptions_by_breed'), # noqa E501 
]
