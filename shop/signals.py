from django.dispatch import receiver, Signal
from django.contrib.auth import get_user_model
from django.db.models.signals import (
    post_save,
    pre_delete
)

from .models import (
    Shop,
    ShopAnalytics,
    ShopStyle,
    Visit,
    Product
)


# Custom signals
object_viewed = Signal(providing_args=['instance'])


@receiver(post_save, sender=Shop)
def _on_shop_create(sender, instance, created, **kwargs):
    # print(kwargs)
    if created:
        # print(f'Setting up {instance}...')
        analytics = ShopAnalytics.objects.create()
        style = ShopStyle.objects.create()
        instance.analytics = analytics
        instance.style = style
        # Set the owner's account type to being a mercahnt
        instance.owner.account_type = get_user_model().MERCHANT
        # print('Shop set up complete!')


@receiver(pre_delete, sender=Shop)
def _on_shop_deleted(sender, instance, **kwargs):
    # print(kwargs)
    # print(f'Deleting {instance}...')
    # print(f'Deleting existing helper Models for {instance}')
    
    # Delete shop analytics
    if instance.analytics:
        instance.analytics.delete()
    # Delete shop style
    if instance.style:
        instance.style.delete()


# curcular import, these signals are probably not even needed
# for this type of visit implementation
# @receiver(object_viewed, sender=Shop)
# def _on_shop_viewed(sender, instance, **kwargs):
#     if instance:
#         Visit.objects.create(
#             shop_analytics=instance.analytics,
#             model=Visit.SHOP,
#             model_id=instance.id
#         )


# @receiver(object_viewed, sender=Product)
# def _on_product_viewed(sender, instance, **kwargs):
#     if instance:
#         Visit.objects.create(
#             shop_analytics=instance.shop.analytics,
#             model=Visit.PRODUCT,
#             model_id=instance.id
#         )
