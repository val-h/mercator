from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

from .models import Shop, Order, Shipment, ShopAnalytics, ShopStyle, Product
from django.contrib.auth import get_user_model


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

def orders(request):
    if request.method == 'GET':
        try:
            orders = request.user.shop.orders.all()
            if orders.count() > 0:
                return JsonResponse({
                    'orders': [order.serialize() for order in orders]
                }, status=200)
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            messages = ['No available orders for this shop.']
            status = 404

    elif request.method == 'POST':
        # attributes 
        # required - customer_id, items: [id, quantity]
        # optional - status: default, Order.PLACED
        data = json.loads(request.body)
        try:
            customer = get_user_model().objects.get(id=data['customer_id'])
            # Attempt to create the order
            order = Order.objects.create(
                customer=customer,
                shop=request.user.shop
            )
            print('created order')

            # Attempt to add the products to the order
            for product_data in data['items']:
                product = Product.objects.get(id=int(product_data['id']))
                for _ in range(product_data['quantity']):
                    order.items.add(product)
            print('added products')

            # Probably not even needed her but in the put method
            # # This section gives out troubles, fix it
            # # Attempt to change the status of the order if applicable
            # if hasattr(data, 'status'):
            #     print('passed first check')
            #     if data['status'] in [option[0] for option in Order.ORDER_OPTIONS]:
            #         order.status = data['status']
            #         print('changed status')
            #     else:
            #         raise ValidationError
            #         # raise ValidationError('Invalid status field.')
            # print('passed status')

            # Validate the order
            order.full_clean()
            print('validated')

            order.save()
            messages = ['Order placed successfuly.']
            status = 201
        except ValidationError:
            messages = ['Invalid field type']
            status = 400
        except Exception:
            messages = ['Bad request.']
            status = 400

    else:
        messages = ['Unsuported request method.']
        status = 405
    
    return JsonResponse({
        'messages': messages
    }, status=status)

def order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'GET':
        return JsonResponse({
            'order': order.serialize()
        }, status=200)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        try:
            # Attempt to update the order
            for field, value in data.items():
                if field in Order.CONFIGURABLE_FIELDS:
                    print(f'setting {field} with value {value}')
                    setattr(order, field, value)

            # Validate the order
            order.full_clean()

            order.save()
            messages = ['Order successfuly updated.']
            status = 200
        except ValidationError:
            messages = ['Invalid field type']
            status = 400
        except Exception:
            messages = ['Bad request.']
            status = 400

    elif request.method == 'DELETE':
        order.delete()
        messages = ['Order successfuly deleted.']
        status = 200

    else:
        messages = ['Unsuported request method.']
        status = 405
    
    return JsonResponse({
        'messages': messages
    }, status=status)