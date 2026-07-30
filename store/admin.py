# store/admin.py
from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem

# 1. Keep or update your existing Product registration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_available']
    list_editable = ['price', 'stock', 'is_available']
    search_fields = ['name']

# 2. Register CartItem so you can monitor what people are holding
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']
    list_filter = ['created_at']

# 3. Use an Inline configuration so Order Items display directly inside the Order view page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Prevents displaying empty filler rows
    readonly_fields = ['product_name', 'price', 'quantity']

# 4. Register Orders with a rich dashboard management table view
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status'] # Allows you to mark an order as "Shipped" or "Delivered" with one click
    search_fields = ['id', 'user__username', 'stripe_payment_intent_id']
    inlines = [OrderItemInline]
