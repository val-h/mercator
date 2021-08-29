from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_preference_value(value):
    if value < 0 or value > 3:
        raise ValidationError(_(f'{value} should be between 0 and 3.'))


def validate_preference_search_modifier(value):
    if value < 0 or value > 5:
        raise ValidationError(_(f'{value} should be between 0 and 5.'))
