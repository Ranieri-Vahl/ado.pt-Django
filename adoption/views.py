from django.shortcuts import render

from publish.models import DogBreed, Pet


def list_pets(request):
    pets = Pet.objects.filter(status="F")
    dogbreed = DogBreed.objects.all()

    city = request.GET.get('city')
    breed = request.GET.get('dogbreed')

    if city:
        pets = Pet.objects.filter(city=city)
    
    if breed:
        
        pets = Pet.objects.filter(dogbreed__id=breed)
        breed = DogBreed.objects.get(id=breed)
        
    return render(request, 'adoption/list_pets.html', context={
        'pets': pets,
        'dogbreeds': dogbreed,
        'city': city,
        'breed': breed,
    })
