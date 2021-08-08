from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Shop, Product


def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        if products.count() > 0:
            return JsonResponse({
                'products': [product.serialize() for product in products]
            })
        else:
            return JsonResponse({
                'message': 'No products available.'
            })
    # Working with  both form-data and plain JSON data
    elif request.method == 'POST' and request.user.shop:
        # data = request.POST
        data = json.loads(request.body)
        try:
            new_product = Product.objects.create(
                shop=request.user.shop,
                title=data['title'],
                description=data['description'],
                price=data['price'],
                quantity=data['quantity'])
            new_product.save()
        except Exception:
            message = 'Failed to create the product.'
        finally:
            message =  'Successful POST request!'
        return JsonResponse({
            'message': message,
            'data': data
        })

    else:
        return JsonResponse({
            'message': 'Unsuported request method.'
        })

def product(request, id):
    try:
        product = Product.objects.get(pk=id)
    except ObjectDoesNotExist:
        message = 'Object does not exist.'
    else:
        if request.method == 'GET':
            return JsonResponse({
                'product': product.serialize()
            })
        elif request.user != product.shop.owner:
            message = 'Access denied.'
        elif request.method == 'PUT':
            data = json.loads(request.body)
            try:
                for field, value in data.items():
                    setattr(product, field, value)
                product.save()
            except Exception:
                message = 'Could not update the product.'
            else:
                message = 'Product updated successfuly.'
        elif request.method == 'DELETE':
            product.delete()
            message = 'Product successfuly deleted.'
            
        else:
            message = 'Unsuported request method.'
    
    return JsonResponse({
        'message': message
    })
        