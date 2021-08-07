from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import Shop, Product


def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return JsonResponse({
            'products': [product.serialize() for product in products]
        })
    # Working with  both form-data and plain JSON data
    elif request.method == 'POST' and request.user.shop:
        # data = request.POST
        data = json.loads(request.body)
        return JsonResponse({
            'message': 'Successful POST request!',
            'data': data
        })

    else:
        return JsonResponse({
            'message': 'Unsuported request method.'
        })

def product(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'GET':
        return JsonResponse({
            'product': product.serialize()
        })
    elif request.user != product.shop.owner:
        return JsonResponse({
            'message': 'Access denied.'
        })
    elif request.method == 'PUT':
        pass
    elif request.method == 'PATCH':
        pass
    elif request.method == 'DELETE':
        pass

    else:
        return JsonResponse({
            'message': 'Unsuported request method.'
        })
        