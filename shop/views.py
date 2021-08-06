from django.shortcuts import render
from django.http import JsonResponse

from .models import Shop, Product


def products(request, id=None):
    if request.METHOD == 'GET':
        if id:
            product = Product.objects.get(id)
            return JsonResponse({
                'product': product.serilize()
            })
