from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
import json

from users.models import CustomUser
from .models import Review, Order, Shipment, Product, Item


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
            messages = ['User  updated.']
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
        messages = ['User  deleted.']
        status = 200

    else:
        messages = ['Unsupported request method.']
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
                'messages': ['There are no reviews from this user.']
            }, status=404)

    else:
        return JsonResponse({
            'messages': ['Unsupported request method.']
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
                'messages': ['There are no orders from this user.']
            }, status=404)

    else:
        return JsonResponse({
            'messages': ['Unsupported request method.']
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
                'messages': ['There are no shipments from this user.']
            }, status=404)

    else:
        return JsonResponse({
            'messages': ['Unsupported request method.']
        }, status=405)


def cart_items(request):
    user = request.user

    if request.method == 'GET':
        cart_items = user.cart.serialize()
        if len(cart_items) > 0:
            return JsonResponse({
                'cart-items': cart_items
            }, status=200)

        else:
            return JsonResponse({
                'messages': ['There are no items in the cart of the user.']
            }, status=404)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        messages = []
        try:
            # O(n2) - look for a more elegant way to solve this for both

            # Attempt to update the cart
            if 'items_to_remove' in data:
                for item_details in data['items_to_remove']:
                    for item in user.cart.items.all():
                        if item_details['id'] == item.product.id:
                            item.quantity -= int(item_details['quantity'])
                            if item.quantity < 1:
                                # Remove the item from the cart and delkete it
                                user.cart.items.remove(item)
                                item.delete()
                            else:
                                # Validate and save the item
                                item.full_clean()
                                item.save()

            # Update works, refine it and refactor the other endpoints
            if 'items_to_add' in data:
                for item_details in data['items_to_add']:
                    for item in user.cart.items.all():
                        if item_details['id'] == item.product.id:
                            item.quantity += int(item_details['quantity'])
                            if item.quantity > item.product.available_quantity:
                                messages += ['Not enough ']
                                raise Exception
                            # Validate and save the item
                            item.full_clean()
                            item.save()
                        else:
                            item = Item.objects.create(
                                product=Product.objects.get(
                                    id=item_details['id']
                                ),
                                quantity=item_details['quantity'],
                                cart=user.cart
                            )
                            # Validate the item
                            item.full_clean()
                            user.cart.items.add(item)

            # Validate cart
            user.cart.full_clean()

            user.cart.save()
            messages += ['Cart updated.']
            status = 200
        except ValidationError:
            messages += ['Invalid field type']
            status = 400
        except Exception:
            messages += ['Bad request.']
            status = 400

    # Just clear the cart
    elif request.method == 'DELETE':
        user.cart.clear()
        messages = ['Cart  cleared.']
        status = 200

    else:
        messages = ['Unsupported request method.']
        status = 405

    return JsonResponse({
        'messages': messages
    }, status=status)


def user_type(request):
    if request.method == 'GET':
        return JsonResponse({
            'account_type': request.user.get_account_type_display()
        }, status=200)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        try:
            # Attempt to change the user type
            if 'account_type' in data:
                if data['account_type'].lower() == 'customer':
                    request.user.convert_to_customer()
                elif data['account_type'].lower() == 'merchant':
                    request.user.convert_to_merchant()

            # Validate user
            request.user.full_clean()

            request.user.save()
            messages = ['Account type successfully changed.']
            status = 200
        except ValidationError:
            messages = ['Invalid field type.']
            status = 400
        except Exception:
            messages = ['Bad request.']
            status = 400

    else:
        messages = ['Unsupported request method.']
        status = 405

    return JsonResponse({
        'messages': messages
    }, status=status)
