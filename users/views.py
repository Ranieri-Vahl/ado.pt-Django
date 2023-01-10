from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import redirect, render


def register_view(request):
    if request.user.is_authenticated:  
        return redirect('publish/new_pet')

    if request.method == 'GET':
        return render(request, 'users/register.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(name.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0: # noqa E501
            messages.add_message(
                request, constants.ERROR, 'All fields are required!'
                )
            return render(request, 'users/register.html')

        if password != confirm_password:
            messages.add_message(
                request, constants.ERROR, 'The passwords must be equal!'
                )
            return render(request, 'users/register.html')

        try:
            User.objects.create_user(
                username=name,
                email=email,
                password=password,
            )
            messages.add_message(
                request, constants.SUCCESS, 'Registered with sucess!'
                )
            return render(request, 'users/register.html')

        except User.DoesNotExist:
            messages.add_message(
                request, constants.ERROR, 'Intern error'
                )            
            return render(request, 'users/register.html')


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