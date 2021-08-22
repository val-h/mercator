from django.urls import path

from . import product_views, shop_views, user_views, util_views

app_name = 'shop'
urlpatterns = [
    # Product
    path('products/', product_views.products, name='products'),
    path('products/<int:id>/', product_views.product, name='product'),
    path(  # All reviews for a product
        'products/<int:product_id>/reviews/',
        product_views.product_reviews,
        name='product_reviews'
    ),
    path(  # Single review for a product
        'products/<int:product_id>/reviews/<int:review_id>/',
        product_views.product_review,
        name='product_review'
    ),

    # Shop
    path('shop/', shop_views.shop, name='shop'),
    path('shop/orders/', shop_views.orders, name='shop_orders'),
    path('shop/orders/<int:order_id>/', shop_views.order, name='shop_order'),
    path('shop/shipments/', shop_views.shipments, name='shop_shipments'),
    path(
        'shop/shipments/<int:shipment_id>/',
        shop_views.shipment,
        name='shop_shipment'
    ),
    path('shop/style/', shop_views.style, name='shop_style'),
    path('shop/analytics/', shop_views.analytics, name='shop_analytics'),
    path(
        'shop/analytics/products/<int:id>',
        shop_views.analytics_product,
        name='shop_analytics_product'
    ),

    # User
    path('user/', user_views.user, name='user'),
    path('user/reviews/', user_views.reviews, name='user-reviews'),
    path('user/orders/', user_views.orders, name='user-orders'),
    path('user/shipments/', user_views.shipments, name='user-shipments'),
    path('user/cart-items/', user_views.cart_items, name='user-cart'),
    path('user/type/', user_views.user_type, name='user-type'),

    # Category - TODO
    path('categories/', util_views.categories, name='categories'),
]
