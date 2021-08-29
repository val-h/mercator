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
    Category,
    # Visit,
    # Product,
    Cart
)

from users.models import Preference

User = get_user_model()

# Custom signals
object_viewed = Signal(providing_args=['instance'])


@receiver(post_save, sender=Shop)
def _on_shop_created(sender, instance, created, **kwargs):
    if created:
        analytics = ShopAnalytics.objects.create()
        style = ShopStyle.objects.create()
        instance.analytics = analytics
        instance.style = style
        # Set the owner's account type to being a mercahnt
        instance.owner.convert_to_merchant()


@receiver(pre_delete, sender=Shop)
def _on_shop_deleted(sender, instance, **kwargs):
    # Delete shop analytics
    if instance.analytics:
        instance.analytics.delete()
    # Delete shop style
    if instance.style:
        instance.style.delete()

    instance.owner.convert_to_customer()


# Create a Cart and preference objects for the user automatically
@receiver(post_save, sender=User)
def _on_user_created(sender, instance, created, **kwargs):
    if created:
        # Cart
        _ = Cart.objects.create(user=instance)

        #  Preferences
        for cat in Category.objects.all():
            Preference.objects.create(category=cat, user=instance)


@receiver(pre_delete, sender=User)
def _on_user_deleted(sender, instance, **kwargs):
    # Clear and Remove the cart
    instance.cart.clear()
    instance.cart.delete()

    # Delete all the preferences for this user
    for pref in instance.preferences.all():
        pref.delete()


# On each new category created, make a preference for each yser
@receiver(post_save, sender=Category)
def _on_category_created(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            Preference.objects.create(
                user=user,
                category=instance,
            )


@receiver(pre_delete, sender=Category)
def _on_category_deleted(sender, instance, **kwargs):
    for user in User.objects.all():
        preference = user.preferences.get(category=instance)
        preference.delete()


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
