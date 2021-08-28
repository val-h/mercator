from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

from .models import Product, Review


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
                available_quantity=data['quantity'])

            # Validate the product
            new_product.full_clean()

            new_product.save()
            messages = ['Product successfuly created.']
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
                    if field in Product.CONFIGURABLE_FIELDS:
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


def product_reviews(request, product_id):
    if request.method == 'GET':
        # product = Product.objects.get(product_id)
        reviews = Review.objects.filter(product__id=product_id)
        if reviews.count() > 0:
            return JsonResponse({
                'reviews': [review.serialize() for review in reviews]
            }, status=200)
        else:
            messages = ['No available reviews for this product.']
            status = 404

    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Attempt to create a review
            review = Review.objects.create(
                product=Product.objects.get(id=product_id),
                user=request.user,
                text=data['text']
            )

            # Validate
            review.full_clean()

            review.save()
            messages = ['Review successfuly created.']
            status = 200
        except ValidationError:
            messages = ['Invalid field data.']
            status = 400
        except ObjectDoesNotExist:
            messages = ['Product with that id does not exist.']
            status = 404

    else:
        messages = ['Unsuported request method.']
        status = 405

    return JsonResponse({
        'messages': messages
    }, status=status)


def product_review(request, product_id, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except ObjectDoesNotExist:
        messages = ['Review does not exist for that product.']
        status = 404
    else:
        if request.method == 'GET':
            return JsonResponse({
                'review': review.serialize()
            }, status=200)

        elif request.method == 'PUT':
            data = json.loads(request.body)
            try:
                # Attempt to update the review
                for field, value in data.items():
                    if field in Review.CONFIGURABLE_FIELDS:
                        setattr(review, field, value)

                # Validate
                review.full_clean()

                review.save()
                messages = ['Review successfuly updated.']
                status = 200
            except ValidationError:
                messages = ['Invalid field data.']
                status = 400
            except Exception:
                messages = ['Could not update the product.']
                status = 400

        elif request.method == 'DELETE':
            review.delete()
            messages = ['Review successfuly deleted.']
            status = 200

        else:
            messages = ['Unsuported request method.']
            status = 405

    return JsonResponse({
        'messages': messages
    }, status=status)
