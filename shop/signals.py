from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_delete
)

from .models import (
    Shop,
    ShopAnalytics,
    ShopStyle,
    Visit,
)


@receiver(post_save, sender=Shop)
def _on_shop_create(sender, instance, created, **kwargs):
    # print(kwargs)
    if created:
        # print(f'Setting up {instance}...')
        analytics = ShopAnalytics.objects.create()
        style = ShopStyle.objects.create()
        instance.analytics = analytics
        instance.style = style
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
