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

            # Attempt to add the products to the order
            for product_data in data['items']:
                product = Product.objects.get(id=int(product_data['id']))
                for _ in range(product_data['quantity']):
                    order.items.add(product)

            # Update the optional fields
            for field, value in data.items():
                if field in Order.CONFIGURABLE_FIELDS:
                    setattr(order, field, value)

            # Validate the order
            order.full_clean()

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
    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        messages = ['Order with that id does not exist.']
        status = 404
    else:
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


def shipments(request):
    if request.method == 'GET':
        try:
            shipments = Shipment.objects.all()
            if shipments.count() > 0:
                return JsonResponse({
                    'shipments': [
                        shipment.serialize() for shipment in shipments
                    ]
                }, status=200)
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            messages = ['No available shipments for this shop.']
            status = 404

    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Get the standing order
            order = Order.objects.get(id=data['order_id'])
            # Attempt to create a shipment
            shipment = Shipment.objects.create(
                order=order,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                company=data['company'],
                address=data['address'],
                post_code=data['post_code'],
                state=data['state'],
                city=data['city'],
                country=data['country'],
                contact_number=data['contact_number']
            )

            # Validate the shipment
            shipment.full_clean()

            shipment.save()
            messages = ['Shipment successfuly created.']
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


def shipment(request, shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except ObjectDoesNotExist:
        messages = ['Shipment does not exist.']
        status = 404
    except Exception:
        messages = ['Some wierd exception.']
        status = 400
    else:
        if request.method == 'GET':
            return JsonResponse({
                'shipment': shipment.serialize()
            }, status=200)

        elif request.method == 'PUT':
            data = json.loads(request.body)
            try:
                # Attempt to change the details in the shipment
                for field, value in data.items():
                    if field in Shipment.CONFIGURABLE_FIELDS:
                        setattr(shipment, field, value)

                # Validate shipment
                shipment.full_clean()

                shipment.save()
                messages = ['Shipment successfuly updated.']
                status = 200
            except ValidationError:
                messages = ['Invalid field type']
                status = 400
            except Exception:
                messages = ['Bad request.']
                status = 400

        elif request.method == 'DELETE':
            shipment.delete()
            messages = ['Shipment successfuly deleted.']
            status = 200

        else:
            messages = ['Unsuported request method.']
            status = 405

    return JsonResponse({
        'messages': messages
    }, status=status)


def style(request):
    try:
        style = ShopStyle.objects.get(shop__owner=request.user)
    except ObjectDoesNotExist:
        messages = ['Shop does not exist.']
        status = 404
    else:
        if request.method == 'GET':
            return JsonResponse({
                'style': style.serialize()
            }, status=200)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            try:
                # Attempt to update the style
                for field, value in data.items():
                    if field in ShopStyle.CONFIGURABLE_FIELDS:
                        setattr(style, field, value)

                # Validate the style
                style.full_clean()

                style.save()
                messages = ['Style successfuly updated.']
                status = 200
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

def analytics(request):
    pass
