from django.urls import path # type: ignore
from .views import home, about, contact, shop, cart, checkout # type: ignore

urlpatterns = [
    path('', home, name='home'),
    path('/about', about, name='about'),
    path('/contact', contact, name='contact'),
    path('/shop', shop, name='shop'),
    path('/cart', cart, name='cart'),
    path('/checkout', checkout, name='checkout')
]