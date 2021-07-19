from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add preferences, acc type, other stats
    # stats, should have been positive integer field
    total_reviews = models.IntegerField(default=0) 
    total_items_bought = models.IntegerField(default=0)
    is_shop_owner = models.BooleanField(default=False)

    CUSTOMER = 'C'
    MERCHANT = 'M'
    ACCOUNT_TYPE_OPTIONS = [
        (CUSTOMER, 'Customer'),
        (MERCHANT, 'Merchant')
    ]
    account_type = models.CharField(
        max_length=1,
        choices=ACCOUNT_TYPE_OPTIONS,
        default=CUSTOMER)

    # preferences = models.ForeignKey()
