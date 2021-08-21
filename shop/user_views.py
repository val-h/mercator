from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import logout
import json

from users.models import CustomUser
from .models import Review, Order, Shipment, Cart


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
