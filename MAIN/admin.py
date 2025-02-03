from django.contrib import admin
# admin.py

admin.site.site_header = "MA TARA ADMIN"
admin.site.site_title = "MA TARA ADMIN"
admin.site.index_title = "Dashboard"
from .models import *

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

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'payment_date', 'status')
    list_filter = ('status',)

class ContactAdmin(admin.ModelAdmin):
    # Define the fields to display in the list view
    list_display = ('name', 'phone_number', 'number_of_prints', 'delivery_date', 'product', 'delivery_location')
    
    # Add search functionality to the admin panel
    search_fields = ('name', 'phone_number', 'product')
    
    # Optionally, add filter options in the sidebar
    list_filter = ('delivery_location', 'product')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Contact)
admin.site.register(Category)

# Register your models here.
