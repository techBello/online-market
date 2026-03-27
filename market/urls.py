from django.urls import path # type: ignore
from .views import stripe_webhook, create_checkout_session, home, about, contact, shop, cart, checkout, create_checkout_session, payment_success, payment_cancel, add_to_cart, add_to_wishlist # type: ignore

urlpatterns = [
    path('', home, name='home'),
    path('/about', about, name='about'),
    path('/contact', contact, name='contact'),
    path('/shop', shop, name='shop'),
    path('/cart', cart, name='cart'),
    path('/add-to-cart/', add_to_cart, name='add_to_cart'),
    path('/add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    # path('/checkout', checkout, name='checkout'),
    path('/checkout', create_checkout_session, name='checkout'),
    path('/success', payment_success, name='payment_success'),
    path('/cancel', payment_cancel, name='payment_cancel'),
    path('/webhook', stripe_webhook, name='stripe_webhook'),
]


