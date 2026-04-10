from django.shortcuts import render, redirect # type: ignore
import stripe # type: ignore
from django.conf import settings # type: ignore
from django.shortcuts import redirect # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.urls import reverse # type: ignore
from django.db.models import Q, Min, Max # type: ignore
from .models import Product, Category, ProductImage, Cart, CartItem, ProductSKU # type: ignore
import json # type: ignore

# Create your views here.
def home(request):
    featured_products = Product.objects.filter(is_active=True).prefetch_related('images', 'skus')[:8]
    categories = Category.objects.all()[:12]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    products = Product.objects.filter(is_active=True).prefetch_related('images', 'skus')
    categories = Category.objects.all()
    
    # Get price range
    price_range = ProductSKU.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        products = products.filter(category__slug=category)
    
    # Filter by price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(skus__price__gte=min_price)
    if max_price:
        products = products.filter(skus__price__lte=max_price)
    
    # Search
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Sort
    sort_by = request.GET.get('sort', 'latest')
    if sort_by == 'price_low':
        products = products.order_by('skus__price')
    elif sort_by == 'price_high':
        products = products.order_by('-skus__price')
    elif sort_by == 'popular':
        products = products.order_by('-created_at')
    else:  # latest
        products = products.order_by('-created_at')
    
    products = products.distinct()
    
    context = {
        'products': products,
        'categories': categories,
        'price_range': price_range,
        'selected_category': category,
        'selected_sort': sort_by,
        'search_query': search_query or '',
    }
    return render(request, 'shop.html', context)

def checkout(request):
    user = request.user if request.user.is_authenticated else None
    cart_items = []
    total_price = 0
    
    if user:
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.select_related('sku__product').all()
            total_price = sum(item.sku.price * item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            pass
    
    success_url = request.build_absolute_uri(
        reverse("payment_success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'success_url': success_url,
    }
    return render(request, 'checkout.html', context)

def cart(request):
    user = request.user if request.user.is_authenticated else None
    cart_items = []
    
    if user:
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.select_related('sku__product').all()
        except Cart.DoesNotExist:
            pass
    
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)

@csrf_exempt
def add_to_cart(request): # add to cart function
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            
            user = request.user if request.user.is_authenticated else None
            
            if not user:
                return JsonResponse({'success': False, 'message': 'Please login first'}, status=401)
            
            cart_obj, _ = Cart.objects.get_or_create(user=user)
            
            try:
                sku = ProductSKU.objects.filter(product_id=product_id).first()
                if not sku:
                    return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
                
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart_obj,
                    sku=sku,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                
                return JsonResponse({'success': True, 'message': 'Product added to cart'})
            except ProductSKU.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Product variant not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@csrf_exempt
def add_to_wishlist(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            user = request.user if request.user.is_authenticated else None
            
            if not user:
                return JsonResponse({'success': False, 'message': 'Please login first'}, status=401)
            
            product = Product.objects.get(id=product_id)
            
            # Simple implementation - you can create a Wishlist model later
            message = f'{product.name} added to wishlist!'
            return JsonResponse({'success': True, 'message': message})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

# Stripe payment view
stripe.api_key = settings.STRIPE_SECRET_KEY # Set your Stripe secret key from settings

def create_checkout_session(request): # create checkout session for Stripe payment
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
            return render(request, 'checkout.html')
    return render(request, 'checkout.html')

def payment_success(request):
    session_id = request.GET.get("session_id")
    return render(request, "success.html", {"session_id": session_id})

def payment_cancel(request):
    return render(request, "cancel.html")


@csrf_exempt
def stripe_webhook(request): # handle Stripe webhook events
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return JsonResponse({'error': 'Invalid webhook'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # ✅ Here you mark order as paid
        # Example:
        # order = Order.objects.get(id=session.client_reference_id)
        # order.paid = True
        # order.save()

    return JsonResponse({'status': 'success'})
