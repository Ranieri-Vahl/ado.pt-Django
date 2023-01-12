from django.shortcuts import render
from publish.models import Pet, DogBreed


def list_pets(request):
    pets = Pet.objects.filter(status="F")
    dogbreed = DogBreed.objects.all()
    return render(request, 'adoption/list_pets.html', context={
        'pets': pets,
        'dogbreeds': dogbreed,
    })
