from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from adoption.models import RequestAdoption

from .models import DogBreed, Pet, Tag


@login_required(login_url='/auth/login/')
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


@login_required(login_url='/auth/login/')
def your_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(user=request.user)
        return render(request, 'publish/your_pets.html', context={
            'pets': pets,
        })


@login_required(login_url='/auth/login/')
def remove_pet(request, id_remove):
    pet = Pet.objects.get(id=id_remove)

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


@login_required(login_url='/auth/login/')
def see_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id=id)
        return render(request, 'publish/see_pet.html', context={
            'pet': pet,
        })


@login_required(login_url='/auth/login/')
def see_request_adoption(request):
    if request.method == "GET":
        request_adoption = RequestAdoption.objects.filter(
            pet__user=request.user, status="WA"
            )
        return render(request, 'publish/see_request_adoption.html', context={
            'requests': request_adoption
        })


def dashboard(request):
    if request.method == "GET":
        return render(request, 'publish/dashboard.html')


@csrf_exempt
def api_adoptions_by_breed(request):
    breeds = DogBreed.objects.all()

    qty_adoptions = []
    for breed in breeds:
        adoptions = RequestAdoption.objects.filter(pet__dogbreed=breed).count()
        qty_adoptions.append(adoptions)

    breeds = [breed.dogbreed for breed in breeds]
    data = {
        'qty_adoptions': qty_adoptions,
        'labels': breeds,
    }

    return JsonResponse(data)
