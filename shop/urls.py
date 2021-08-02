from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('shop/', views.shop, name='shop'),

    # API - just a test for now
    path('products/<int:id>', views.products, name='products'),
]
