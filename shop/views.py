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
    elif request.method == 'POST':
        # data = request.POST # For form-data
        data = json.loads(request.body)
        try:
            if not hasattr(request.user, 'shop'):
                raise ObjectDoesNotExist
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
            messages =  ['Product successfuly created.']
            status = 201
        except ValidationError:
            # Send back a message with specific field validation errors
            messages = ['Invalid field data.']
            status = 400
        except ObjectDoesNotExist:
            messages = ['The user is not a merchant. Shop does not exist']
            status = 404
        except Exception:
            messages = ['Failed to create the product.']
            status = 400

        return JsonResponse({
            'messages': messages,
        }, status=status)

    else:
        return JsonResponse({
            'messages': 'Unsuported request method.'
        }, status=405)

def product(request, id):
    try:
        product = Product.objects.get(pk=id)
    except ObjectDoesNotExist:
        messages = ['Object does not exist.']
        status = 404
    else:
        if request.method == 'GET':
            return JsonResponse({
                'product': product.serialize()
            }, status=200)

        # Deny access to any user that is not the owner of the shop
        elif request.user != product.shop.owner:
            messages = ['Access denied.']
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
                messages = ['Product updated successfuly.']
                status = 200
            except ValidationError:
                messages = ['Invalid field data.']
                status = 400
            except Exception:
                messages = ['Could not update the product.']
                status = 400

        elif request.method == 'DELETE':
            product.delete()
            messages = ['Product successfuly deleted.']
            status = 200
            
        else:
            messages = ['Unsuported request method.']
            status = 405
    
    return JsonResponse({
        'messages': messages
    }, status=status)


def shop(request):

    def _get_shop(user):
        nonlocal messages
        nonlocal status
        try:
            shop = Shop.objects.get(owner=user)
        except ObjectDoesNotExist:
            messages = ['The user is not a merchant. Shop does not exist']
            status = 404
        except Exception:
            messages = ['Some wierd error occured.']
            status = 400
        else:
            return shop

    if request.method == 'GET':
        shop = _get_shop(request.user)
        if shop:
            return JsonResponse({
                'shop': shop.serialize()
            }, status=200)

    elif request.method == 'POST':
        if not hasattr(request.user, 'shop'):
            data = json.loads(request.body)
            try:
                # Attempt to create a new shop
                shop = Shop.objects.create(
                    owner=request.user
                )

                # Apply optional fields if present
                for field, value in data.items():
                    if field in Shop.CONFIGURABLE_FIELDS:
                        setattr(shop, field, value)

                # Validate the shop
                shop.full_clean()

                shop.save()
                messages = ['Shop successfuly created.']
                status = 201
            except ValidationError:
                messages = ['Invalid field type']
                status = 400
            except Exception as e:
                # Just to see specific errors
                messages = [f'Exception: {repr(e)}']
                status = 400
        else:
            messages = ['The user already has an open shop.']
            status = 400

    elif request.method == 'PUT':
        shop = _get_shop(request.user)
        data = json.loads(request.body)
        if shop:
            try:
                # Attempt to update the fields
                for field, value in data.items():
                    if field in Shop.CONFIGURABLE_FIELDS:
                        setattr(shop, field, value)

                # Validate the shop
                shop.full_clean()

                shop.save()
                messages = ['Shop successfuly updated.']
                status = 200
            except ValidationError:
                messages = ['Invalid field type']
                status = 400

    elif request.method == 'DELETE':
        shop = _get_shop(request.user)
        if shop:
            shop.delete()
            messages = ['Shop successfuly deleted.']
            status = 200

    else:
        messages = ['Unsuported request method.']
        status = 405
        
    return JsonResponse({
        'messages': messages
    }, status=status)
