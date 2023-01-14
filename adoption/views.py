from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from publish.models import DogBreed, Pet

from .models import RequestAdoption


@login_required
def list_pets(request):
    pets = Pet.objects.filter(status="F")
    dogbreed = DogBreed.objects.all()

    city = request.GET.get('city')
    breed = request.GET.get('dogbreed')

    if breed:             
        pets = Pet.objects.filter(dogbreed__id=breed, city__icontains=city)
        breed = DogBreed.objects.get(id=breed)
   
    dogbreed_all = DogBreed.objects.get(dogbreed='All DogBreeds')
    if dogbreed_all == breed:
        pets = Pet.objects.filter(status="F", city__icontains=city)

    return render(request, 'adoption/list_pets.html', context={
        'pets': pets,
        'dogbreeds': dogbreed,
        'city': city,
        'breed': breed,
    })


@login_required
def request_adoption(request, pet_id):
    pet = Pet.objects.filter(id=pet_id, status="F")

    if not pet.exists():
        messages.add_message(
            request, constants.ERROR, 'This pet is already adopted'
            )
        return redirect('/adoption')

    request_to_adopt = RequestAdoption(
        pet=pet.first(),
        user=request.user,
        date=datetime.now()
    )

    request_to_adopt.save()
    messages.add_message(
        request, constants.SUCCESS, 'Successful adoption request'
        )
    return redirect('/adoption')
