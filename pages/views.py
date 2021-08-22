from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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


@login_required
def account(request):
    return render(request, 'account.html', {
        "user": request.user
    })


def search(request, pattern):
    # Search through the database and display relative information
    return render(request, 'search.html', {
        "pattern": pattern
    })


@login_required
def shop(request):
    shop = request.user.shop
    products = shop.products.all()
    return render(request, 'shop.html', {
        'shop': shop,
        'products': products
    })
