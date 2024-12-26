from django.contrib import admin
# admin.py

from .models import Product, Order, OrderItem, Shipping, Cart, CartItem, Payment

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to show

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'customer')
    inlines = [OrderItemInline]

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order', 'shipping_method', 'shipping_status', 'shipping_date', 'estimated_delivery_date')
    list_filter = ('shipping_status',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'updated_at')
    inlines = [CartItemInline]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'payment_date', 'status')
    list_filter = ('status',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Payment, PaymentAdmin)

# Register your models here.
