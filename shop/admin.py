from django.contrib import admin

from .models import Product, Image, Order, Shipment

# Register your models here.
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(Shipment)
