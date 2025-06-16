from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import User
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    number_of_prints = models.CharField(max_length=10, null=True, blank=True )
    delivery_date = models.DateField( null=True ,blank=True)
    address = models.TextField()
    product = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Contact request from {self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')
    phone = models.CharField(max_length=15, null=True, blank=True)
    # Other fields...
    
    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    
    # Link to Category Model
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    
    size = models.CharField(max_length=50, null=True, blank=True)  # Optional size field for products like T-shirts, posters
    material = models.CharField(max_length=100, null=True, blank=True)  # Material type for products like T-shirts
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
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total GST for the order
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Discount applied to the order
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='Pending')
    
    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"
    
    def calculate_total(self):
        # Calculate total without GST
        self.total_amount = sum(item.get_total_price() for item in self.items.all())
        
        # Calculate GST for the whole order based on the items' GST amounts
        self.gst_amount = sum(item.gst_amount for item in self.items.all())
        
        # Apply discount if applicable
        if self.discount:
            self.total_amount -= self.discount
        
        # Add GST to the total amount
        self.total_amount += self.gst_amount
        self.save()

    def is_paid(self):
        return self.payment_status.lower() == 'paid'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.0)  # GST rate (e.g., 18%)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # GST for this item
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.unit_price

    def calculate_gst(self):
        # GST for this item
        self.gst_amount = (self.get_total_price() * self.gst_rate) / 100
        self.save()


class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=255)
    shipping_date = models.DateTimeField(auto_now_add=True)
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=255, null=True, blank=True)
    shipping_status = models.CharField(max_length=50, default='Not Shipped')
    courier = models.CharField(max_length=100, null=True, blank=True)  # Courier service used
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Shipping cost

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
    transaction_id = models.CharField(max_length=255, null=True, blank=True)  # Optional transaction ID
    gateway = models.CharField(max_length=100, null=True, blank=True)  # Optional payment gateway (e.g., Stripe, PayPal)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery_images/')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
