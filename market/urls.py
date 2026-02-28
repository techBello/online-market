from django.urls import path # type: ignore
from .views import create_checkout_session, home, about, contact, shop, cart, checkout, create_checkout_session, payment_success, payment_cancel # type: ignore

urlpatterns = [
    path('', home, name='home'),
    path('/about', about, name='about'),
    path('/contact', contact, name='contact'),
    path('/shop', shop, name='shop'),
    path('/cart', cart, name='cart'),
    path('/checkout', checkout, name='checkout'),
    path("checkout/", create_checkout_session, name="checkout"),
    path("success/", payment_success, name="payment_success"),
    path("cancel/", payment_cancel, name="payment_cancel"),
]

# path("webhook/", views.stripe_webhook, name="stripe_webhook"),