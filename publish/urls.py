from django.urls import path

from . import views

urlpatterns = [
    path('new_pet/', views.new_pet, name='new_pet'),
    path('your_pets/', views.your_pets, name='your_pets'),
    path('remove_pet/<int:id>', views.remove_pet, name='remove_pet'),    
]
