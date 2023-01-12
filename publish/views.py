from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Tag, DogBreed, Pet


@login_required
def new_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        dogbreeds = DogBreed.objects.all()
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
