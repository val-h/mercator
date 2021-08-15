from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json

from users.models import CustomUser

# User api endpoints
