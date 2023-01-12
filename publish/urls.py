from django.urls import path
from . import views

urlpatterns = [
    path('new_pet/', views.new_pet, name='new_pet')    
]
