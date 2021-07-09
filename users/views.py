from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

from .forms import CustomUserCreateForm
from .models import CustomUser


def register(request):
    """Register view for our app."""
    if request.method == 'GET':
        # The form could be a static one, without passing this
        return render(request, 'registration/register.html', {
            'form': CustomUserCreateForm()
        })
    elif request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password1"]
        confirmation = request.POST["password2"]
        if password != confirmation:
            return render(request, 'registration/register.html', {
                'form': CustomUserCreateForm(request.POST), # prefiled
                'message': 'Passwords must match.'
            })
        
        # Attempt to create a new user
        try:
            user = CustomUser.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'registration/register.html', {
                'form': CustomUserCreateForm(request.POST), # prefiled
                'message': 'Username already taken.'
            })
        login(request, user)
        return redirect('pages:home')
