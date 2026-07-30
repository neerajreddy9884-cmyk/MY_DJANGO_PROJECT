# store/urls.py
from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'store'  # KEEPING YOUR EXACT APP_NAME VARIABLE DEFINITION

urlpatterns = [
    # 1. Your existing product catalog URLs (Modified slightly to match your <int:product_id> views code)
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # 2. Add New Shopping Cart Processing Paths
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # 3. Add New Checkout and Stripe Completion Paths
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-cancelled/', lambda r: render(r, 'store/cancelled.html'), name='payment_cancelled'),
]
