
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import constants
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms.login_form import LoginForm
from .forms.register_form import RegisterForm


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
    else:
        messages.add_message(
            request, constants.ERROR, 'There are errors in the form! Please fix them' # noqa E501
            ) 
    return redirect('register')


def login_view(request):
    form = LoginForm()
    return render(request, 'users/login.html', context={
        'form': form,
        'form_action': reverse('login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get('name'),
            password=form.cleaned_data.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('list_pets')
        else:
            messages.add_message(
                request, constants.ERROR, 'Name or password are invalid!'
                )              
            return redirect('login')
    else:
        messages.add_message(
            request, constants.ERROR, 'Name or password are invalid!'
            ) 


def logout_view(request):
    logout(request)
    return redirect('login')