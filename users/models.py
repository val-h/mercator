from django.contrib.auth.models import AbstractUser
from django.db import models


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

    # preferences = models.ForeignKey()

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
