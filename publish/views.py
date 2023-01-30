from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from adoption.models import RequestAdoption

from .forms.new_pet_form import NewPetForm
from .models import DogBreed, Pet, Tag


@login_required(login_url='/auth/login/')
def new_pet(request):
    newpet_form_data = request.session.get('newpet_form_data', None)
    form = NewPetForm(newpet_form_data)
    tags = Tag.objects.all()
    dogbreeds = DogBreed.objects.all().exclude(dogbreed='All DogBreeds')
    return render(request, 'publish/new_pet.html', context={
        'form': form,
        'tags': tags,
        'dogbreeds': dogbreeds,
        'form_action': reverse('new_pet_create'),
    })


@login_required(login_url='/auth/login/')
def new_pet_create(request):
    if not request.POST:
        raise Http404
    POST = request.POST
    request.session['newpet_form_data'] = POST
    form = NewPetForm(
        data=request.POST,
        files=request.FILES,
        )

    tags = request.POST.getlist('tags')
    dogbreeds = request.POST.get('dogbreeds')

    if form.is_valid():
        petform = form.save(commit=False) 
        phone = request.POST.get('phone_number')
        pet = Pet(            
            user=request.user,
            picture=petform.picture,
            name=petform.name,
            description=petform.description,
            state=petform.state,
            city=petform.city,
            phone_number=phone,
            dogbreed_id=dogbreeds,
        )    
        pet.save()
        
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)

        del (request.session['newpet_form_data'])
        pet.save()

        messages.add_message(
            request, constants.SUCCESS, 'New pet Registered with success!'
        )
        return redirect('your_pets')
    else:
        messages.add_message(
            request, constants.ERROR, 'There are errors in the form! Please fix them' # noqa E501
            )         
    return redirect('new_pet')


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
