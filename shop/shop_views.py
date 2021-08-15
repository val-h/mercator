from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

from .models import Shop


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
