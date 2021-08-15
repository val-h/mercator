from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

from .models import Category


def categories(request):
    if request.method == 'GET':
        # No check for category availability
        # Ensure there are always categories - admin made
        categories = Category.objects.all()
        return JsonResponse({
            'categories': [cat.serialize() for cat in categories]
        }, status=200)
    
    else:
        return JsonResponse({
            'messages': ['Usuported request method']
        }, status=405)
