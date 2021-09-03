from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_review_stars(value):
    if value < 1 or value > 5:
        return ValidationError(
            _(f'Review value - {value} should be between 1 and 5.'))
