from django.contrib import admin

from .models import (
    Product,
    Image,
    Order,
    Shipment,
    Review,
    Cart,
    Visit,
    Shop,
    ShopAnalytics,
    ShopStyle,
    Category,
    Tag
)

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(Shipment)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Visit)
admin.site.register(Shop)
admin.site.register(ShopAnalytics)
admin.site.register(ShopStyle)
admin.site.register(Category)
admin.site.register(Tag)
