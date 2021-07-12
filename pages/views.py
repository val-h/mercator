from django.shortcuts import render


def home(request):
    return render(request, 'home.html', context={})

def categories(request):
    return render(request, 'categories.html', context={})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def cart(request):
    return render(request, 'cart.html', context={})
