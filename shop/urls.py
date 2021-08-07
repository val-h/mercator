from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/<int:id>/', views.product, name='product'),
]
