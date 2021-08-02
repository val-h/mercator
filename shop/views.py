from django.shortcuts import render
from django.http import JsonResponse

from .models import Shop, Product

# Create your views here.
def shop(request):
    shop = Shop.objects.get(owner=request.user)
    products = shop.products.all()
    return render(request, 'shop.html', {
        'shop': shop,
        'products': products
    })

def products(request, id=None):
    if request.METHOD == 'GET':
        if id:
            product = Product.objects.get(id)
            return JsonResponse({
                'product': product.serilize()
            })
