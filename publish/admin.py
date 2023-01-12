from django.contrib import admin

from .models import DogBreed, Pet, Tag

admin.site.register(DogBreed)
admin.site.register(Tag)
admin.site.register(Pet)
