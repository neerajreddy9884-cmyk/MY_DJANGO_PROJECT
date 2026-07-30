from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe

# Import your database models and forms
from .models import Product, CartItem, Order, OrderItem
from .forms import CustomerRegistrationForm

# ==========================================
# 1. PRODUCT CATALOG VIEWS (Your existing type of views)
# ==========================================

def product_list(request):
    """
    Displays all available products to the customers on the front-end.
    """
    products = Product.objects.filter(is_available=True)
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    """
    Displays full details for a single selected product.
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


# ==========================================
# 2. USER AUTHENTICATION VIEWS
# ==========================================

def register(request):
    """
    Handles new customer registration using the form created in forms.py.
    """
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'store/register.html', {'form': form})


# ==========================================
# 3. SHOPPING CART VIEWS
# ==========================================

@login_required
def view_cart(request):
    """
    Displays all items currently inside the logged-in user's cart.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    """
    Adds a single quantity of a product to the user's cart or increments it.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is out of stock before adding
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('product_list')
        
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        # Prevent user from adding more items than what is physically available
        if cart_item.quantity >= product.stock:
            messages.warning(request, f"Cannot add more items. Only {product.stock} units available.")
            return redirect('view_cart')
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('store:view_cart')


@login_required
def remove_from_cart(request, item_id):
    """
    Deletes a specific product record completely from the user's shopping cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from your cart.")
    return redirect('store:view_cart')


# ==========================================
# 4. CHECKOUT & STRIPE PAYMENT VIEWS
# ==========================================

# Initialize Stripe configuration keys from settings.py
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    """
    Compiles cart data, builds a pending order log, and opens a Stripe payment portal.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('store:view_cart')
        
    total = sum(item.total_price() for item in cart_items)
    
    # Create the internal permanent order snapshot record
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status='PENDING',
        shipping_address="User Home Address" # Placeholder string for now
    )
    
    # Mirror items from temporary Cart to permanent Order Items list
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )
    
    try:
        # Build the external checkout session interface redirect configuration
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f"Order Total for Reference #{order.id}"},
                    'unit_amount': int(total * 100), # Stripe accepts calculations in Cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payment-success/{order.id}/'),
            cancel_url=request.build_absolute_uri('/payment-cancelled/'),
        )
        
        # Keep track of payment intent id session code reference point string
        order.stripe_payment_intent_id = session.id
        order.save()
        
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, f"An error occurred during checkout setup: {e}")
        return redirect('store:view_cart')


@login_required
def payment_success(request, order_id):
    """
    Executes order fulfillment, drops product inventories numbers, and wipes the cart clear.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'PENDING':
        order.status = 'PAID'
        order.save()
        
        # Process stock changes safely
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            product = item.product
            product.stock -= item.quantity
            if product.stock <= 0:
                product.stock = 0
                product.is_available = False
            product.save()
            
        # Empty user cart out clean following payment receipt complete verification
        cart_items.delete()
        messages.success(request, "Thank you! Your payment was verified and processing has begun.")
        
    return render(request, 'store/success.html', {'order': order})
