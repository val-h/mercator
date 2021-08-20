from django.urls import path

from . import product_views, shop_views, user_views, util_views

app_name = 'shop'
urlpatterns = [
    # Product
    path('products/', product_views.products, name='products'),
    path('products/<int:id>/', product_views.product, name='product'),
    path( # All reviews for a product
        'products/<int:product_id>/reviews/',
        product_views.product_reviews,
        name='product_reviews'
    ),
    path( # Single review for a product
        'products/<int:product_id>/reviews/<int:review_id>/',
        product_views.product_review,
        name='product_review'
    ),

    # Shop
    path('shop/', shop_views.shop, name='shop'),
    path('shop/orders/', shop_views.orders, name='shop_orders'),
    path('shop/orders/<int:order_id>/', shop_views.order, name='shop_order'),

    # Category - TODO
    path('categories/', util_views.categories, name='categories'),
]
