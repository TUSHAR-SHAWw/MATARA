from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('T', 'T-Shirt'),
        ('B', 'Business Card'),
        ('P', 'Poster'),
        ('M', 'Mug'),
        ('C', 'Custom Design'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='C',  # Default category
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('CXL', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='P',  # Default status
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='Pending')
    
    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"
    
    def calculate_total(self):
        self.total_amount = sum(item.get_total_price() for item in self.items.all())
        self.save()

    def is_paid(self):
        return self.payment_status.lower() == 'paid'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.unit_price


class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=255)
    shipping_date = models.DateTimeField(auto_now_add=True)
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=255, null=True, blank=True)
    shipping_status = models.CharField(max_length=50, default='Not Shipped')

    def __str__(self):
        return f"Shipping for Order #{self.order.id}"


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.customer.username}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"
