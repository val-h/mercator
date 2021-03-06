from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('cart/', views.cart, name='cart'),
    path('account/', views.account, name='account'),
    path('search/<str:pattern>', views.search, name='search'),
    path('shop/', views.shop, name='shop'),
]
