from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    # Product
    path('products/', views.products, name='products'),
    path('products/<int:id>/', views.product, name='product'),
    path( # All reviews for a product
        'products/<int:product_id>/reviews/',
        views.product_reviews,
        name='product_reviews'
    ),
    path( # Single review for a product
        'products/<int:product_id>/reviews/<int:review_id>/',
        views.product_review,
        name='product_review'
    ),

    # Shop
    path('shop/', views.shop, name='shop'),

    # Category - TODO
    path('categories/', views.categories, name='categories'),
]
