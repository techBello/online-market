from django.shortcuts import render, redirect # type: ignore
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    return render(request, 'shop.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')


# Stripe payment view
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.method == "POST":
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Premium Plan',
                            },
                            'unit_amount': 5000,  # $50.00
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('payment_success')
                ),
                cancel_url=request.build_absolute_uri(
                    reverse('payment_cancel')
                ),
            )
            return redirect(checkout_session.url)

        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request'})