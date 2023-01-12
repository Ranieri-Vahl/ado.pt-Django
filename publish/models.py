from django.db import models
from django.contrib.auth.models import User


class DogBreed(models.Model):
    dogbreed = models.CharField(max_length=50)

    def __str__(self):
        return self.dogbreed


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Pet(models.Model):
    choices_status = (('F', 'For adoption'), ('A', 'Adopted'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    picture = models.ImageField(upload_to="pets_picture")
    name = models.CharField(max_length=100)
    description = models.TextField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    tags = models.ManyToManyField(Tag)
    dogbreed = models.ForeignKey(DogBreed, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=1, choices=choices_status, default='F'
        )

    def __str__(self):
        return self.name
