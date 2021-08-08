from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    # Product
    path('products/', views.products, name='products'),
    path('products/<int:id>/', views.product, name='product'),

    # Shop
    path('shop/', views.shop, name='shop'),
]
