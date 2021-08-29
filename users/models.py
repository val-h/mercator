from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .validators import (
    validate_preference_value, validate_preference_search_modifier)


class CustomUser(AbstractUser):
    # Add preferences, acc type, other stats
    # stats, should have been positive integer field
    total_reviews = models.IntegerField(default=0)
    total_items_bought = models.IntegerField(default=0)
    is_shop_owner = models.BooleanField(default=False)

    # return human readable format with get_account_type_display()
    CUSTOMER = 'C'
    MERCHANT = 'M'
    ACCOUNT_TYPE = [
        (CUSTOMER, 'Customer'),
        (MERCHANT, 'Merchant')
    ]
    account_type = models.CharField(
        max_length=1,
        choices=ACCOUNT_TYPE,
        default=CUSTOMER)

    CONFIGURABLE_FIELDS = ['username', 'account_type']

    def __str__(self):
        return f'{self.username}'

    def convert_to_customer(self):
        self.is_shop_owner = False
        self.account_type = self.CUSTOMER

    def convert_to_merchant(self):
        self.is_shop_owner = True
        self.account_type = self.MERCHANT

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_shop_owner': self.is_shop_owner,
        }


# Automatically created on each new category with signals
class Preference(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='preferences')
    user_value = models.PositiveSmallIntegerField(
        default=1, validators=[validate_preference_value])  # max 3

    from shop.models import Category
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, editable=False)

    last_search = models.DateTimeField(null=True, blank=True)
    search_modifier = models.PositiveSmallIntegerField(
        default=0, validators=[validate_preference_search_modifier])  # max 5

    CONFIGURABLE_FIELDS = ['user_value']

    def __str__(self):
        return f'{self.user}\'s {self.category} category preference.'

    # To be called on every matching search by category
    def update(self):
        if self.last_search:
            time_difference = timezone.now() - self.last_search
            if time_difference.days() > 7:
                self.search_modifier -= 1
            elif time_difference.days() > 30:
                self.search_modifier -= 2
            elif time_difference.days() > 90:
                self.search_modifier -= 3
            elif time_difference.days() > 180:
                self.search_modifier = 0
            self.search_modifier = max(0, self.search_modifier)
        self.last_search = timezone.now()
        self.search_modifier += 1
        self.search_modifier = min(5, self.search_modifier)

        # Validate and save the preference
        self.full_clean()
        self.save()

    def serialize(self):
        return {
            'user_value': self.user_value,
            'category': self.category.serialize(),
            'last_search': self.last_search,
            'search_modifier': self.search_modifier
        }
