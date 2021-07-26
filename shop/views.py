from django.shortcuts import render

from .models import Shop

# Create your views here.
def shop(request):
    shop = Shop.objects.get(owner=request.user)
    return render(request, 'shop.html', {
        'shop': shop
    })
