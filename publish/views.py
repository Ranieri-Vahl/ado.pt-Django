from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from .models import DogBreed, Pet, Tag


@login_required
def new_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        dogbreeds = DogBreed.objects.all().exclude(dogbreed='All DogBreeds')
        return render(request, 'publish/new_pet.html', context={
            'tags': tags,
            'dogbreeds': dogbreeds,
        })
    elif request.method == "POST":
        picture = request.FILES.get('picture')
        name = request.POST.get('name')
        description = request.POST.get('description')
        state = request.POST.get('state')
        city = request.POST.get('city')
        phone = request.POST.get('phone_number')
        tags = request.POST.getlist('tags')
        dogbreeds = request.POST.get('dogbreeds')

        # validar os dados

        pet = Pet(
            user=request.user,
            picture=picture,
            name=name,
            description=description,
            state=state,
            city=city,
            phone_number=phone,
            dogbreed_id=dogbreeds
        )

        pet.save()

        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)
        
        pet.save()
    return redirect('/publish/your_pets')


def your_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(user=request.user)
        return render(request, 'publish/your_pets.html', context={
            'pets': pets,
        })


def remove_pet(request, id):
    pet = Pet.objects.get(id=id)

    if not pet.user == request.user:
        messages.add_message(
            request, constants.ERROR, 'This pet is not yours!'
        )
        return redirect('/publish/your_pets')
    
    pet.delete()

    messages.add_message(
        request, constants.SUCCESS, 'Pet removed with success'
        )
    return redirect('/publish/your_pets')
