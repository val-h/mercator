from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import logout
import json

from users.models import CustomUser
from .models import Review, Order, Shipment, Cart, Product


def user(request):
    user = request.user
    if request.method == 'GET':
        return JsonResponse({
            'user': user.serialize()
        })

    # Update user settings
    elif request.method == 'PUT':
        data = json.loads(request.body)
        try:
            # Attempt to update the user settings
            for field, value in data.items():
                if field in CustomUser.CONFIGURABLE_FIELDS:
                    setattr(user, field, value)

            # Validate user
            user.full_clean()

            user.save()
            messages = ['User successfuly updated.']
            status = 200
        except ValidationError:
            messages = ['Invalid field type.']
            status = 400
        except Exception:
            messages = ['Bad request.']
            status = 400

    elif request.method == 'DELETE':
        logout(user)
        user.delete()
        messages = ['User successfuly deleted.']
        status = 200

    else:
        messages = ['Unsuported request method.']
        status = 405

    return JsonResponse({
        'messages': messages
    }, status=status)


def reviews(request):
    user = request.user
    reviews = Review.objects.filter(user=user)

    if request.method == 'GET':
        if len(reviews) > 0:
            return JsonResponse({
                'reviews': [review.serialize() for review in reviews]
            }, status=200)
        
        else:
            return JsonResponse({
                'messages': ['Theree are no reviews from this user.']
            }, status=404)

    else:
        return JsonResponse({
            'messages': ['Unsuported request method.']
        }, status=405)


def orders(request):
    user = request.user
    orders = Order.objects.filter(customer=user)

    if request.method == 'GET':
        if len(orders) > 0:
            return JsonResponse({
                'orders': [order.serialize_for_user() for order in orders]
            }, status=200)
        
        else:
            return JsonResponse({
                'messages': ['Theree are no orders from this user.']
            }, status=404)
    
    else:
        return JsonResponse({
            'messages': ['Unsuported request method.']
        }, status=405)


def shipments(request):
    user = request.user
    shipments = Shipment.objects.filter(order__customer=user)

    if request.method == 'GET':
        if len(shipments) > 0:
            return JsonResponse({
                'shipments': [
                    shipment.serialize_for_user() for shipment in shipments
                ]
            }, status=200)
        
        else:
            return JsonResponse({
                'messages': ['Theree are no shipments from this user.']
            }, status=404)
    
    else:
        return JsonResponse({
            'messages': ['Unsuported request method.']
        }, status=405)


def cart_items(request):
    user = request.user

    if request.method == 'GET':
        cart_items = user.cart.serialize()
        if len(cart_items['items']) > 0:
            return JsonResponse({
                'cart-items': cart_items
            }, status=200)
        
        else:
            return JsonResponse({
                'messages': ['There are no items in the cart of the user.']
            }, status=404)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        try:
            # Attempt to update the cart
            if 'items_to_remove' in data:
                for item_id in data['items_to_remove']:
                    user.cart.items.remove(Product.objects.get(id=item_id))
                    
            if 'items_to_add' in data:
                for item_id in data['items_to_add']:
                    user.cart.items.add(Product.objects.get(id=item_id))

            # Validate cart
            user.cart.full_clean()

            user.cart.save()
            messages = ['Cart successfuly updated.']
            status = 200
        except ValidationError:
            messages = ['Invalid field type']
            status = 400
        except Exception:
            messages = ['Bad request.']
            status = 400

    # Just clear the cart
    elif request.method == 'DELETE':
        user.cart.clear()
        messages = ['Cart successfuly cleared.']
        status = 200

    else:
        return JsonResponse({
            'messages': ['Unsuported request method.']
        }, status=405)

    return JsonResponse({
        'messages': messages
    }, status=status)
