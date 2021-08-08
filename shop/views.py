from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

from .models import Shop, Product


def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        if products.count() > 0:
            return JsonResponse({
                'products': [product.serialize() for product in products]
            }, status=200)
        else:
            return JsonResponse({
                'messages': ['No products available.']
            }, status=204)

    # Working with  both form-data and plain JSON data
    elif request.method == 'POST' and request.user.shop:
        # data = request.POST # For form-data
        data = json.loads(request.body)
        try:
            # Attempt to create a new product from the POST data
            new_product = Product.objects.create(
                shop=request.user.shop,
                title=data['title'],
                description=data['description'],
                price=data['price'],
                quantity=data['quantity'])

            # Validate the product
            new_product.full_clean()

            new_product.save()
            message_dict =  ['Successful POST request!']
            status = 201
        except ValidationError as e:
            # Send back a message with specific field validation errors
            message_dict = ['Invalid field data.', *e]
            status = 400
        except Exception:
            message_dict = ['Failed to create the product.']
            status = 400

        return JsonResponse({
            'messages': message_dict,
            # 'data': data,
        }, status=status)

    else:
        return JsonResponse({
            'messages': 'Unsuported request method.'
        }, status=405)

def product(request, id):
    try:
        product = Product.objects.get(pk=id)
    except ObjectDoesNotExist:
        message_dict = ['Object does not exist.']
        status = 404
    else:
        if request.method == 'GET':
            return JsonResponse({
                'product': product.serialize()
            }, status=200)

        # Deny access to any user that is not the owner of the shop
        elif request.user != product.shop.owner:
            message_dict = ['Access denied.']
            status = 403

        # Gives errors on the decimal price field
        # If the data is sent as a string it doesn't have a problem with it
        elif request.method == 'PUT':
            data = json.loads(request.body)
            try:
                # Update each of the attributes provided in the request
                for field, value in data.items():
                    setattr(product, field, value)
                
                # Validate the product
                product.full_clean()

                product.save()
                # product.save(update_fileds=[*data.keys()])
                message_dict = ['Product updated successfuly.']
                status = 200
            except ValidationError as e:
                message_dict = ['Invalid field data.', *e]
                status = 400
            except Exception:
                message_dict = ['Could not update the product.']
                status = 400

        elif request.method == 'DELETE':
            product.delete()
            message_dict = ['Product successfuly deleted.']
            status = 200
            
        else:
            message_dict = ['Unsuported request method.']
            status = 405
    
    return JsonResponse({
        'messages': message_dict
    }, status=status)
        