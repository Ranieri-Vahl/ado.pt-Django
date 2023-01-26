
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms.register_form import RegisterForm
from django.http import Http404


def home(request):
    if request.method == "GET":
        return redirect('adoption/')


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'users/register.html', context={
        'form': form,
        'form_action': reverse('register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.add_message(
            request, constants.SUCCESS, 'User registered with sucess!, Please Log In.' # noqa E501
            ) 
        del (request.session['register_form_data'])
        return redirect('login')

    return redirect('register')


def login_view(request):
    if request.user.is_authenticated:  
        return redirect('publish/new_pet')

    if request.method == "GET":
        return render(request, 'users/login.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(
            username=name,
            password=password,
        )
        if user is not None:
            login(request, user)
            return redirect('/publish/new_pet')
        else:
            messages.add_message(
                request, constants.ERROR, 'User or password are invalid!'
                )              
            return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('/auth/login')