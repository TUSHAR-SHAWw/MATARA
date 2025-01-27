from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category
from .forms import ProductSearchForm

def pricing(request):
    products = Product.objects.all()  # Default to showing all products
    form = ProductSearchForm(request.GET)
    
    if form.is_valid():
        category_id = form.cleaned_data.get('category')
        price = form.cleaned_data.get('price')

        # Filter by category if selected
        if category_id:
            products = products.filter(category_id=category_id)
        
        # Filter by price if selected
        if price:
            if price == '100':
                products = products.filter(price__gte=100, price__lte=250)
            elif price == '250':
                products = products.filter(price__gte=250, price__lte=500)
            elif price == '500':
                products = products.filter(price__gte=500, price__lte=1000)
            elif price == '1000':
                products = products.filter(price__gte=1000, price__lte=2500)
            elif price == '2500+':
                products = products.filter(price__gte=2500)
        
        # Optionally, filter by in-stock products only
        products = products.filter(stock__gt=0)

    # Apply pagination: Show only 20 products per page
    paginator = Paginator(products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pricing.html', {'form': form, 'page_obj': page_obj})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Get the form data
            user = form.save(commit=False)  # Don't save the user immediately
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Get the password from the form

            # Check if the username already exists
            if username and User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('MAIN:register')
            if form.cleaned_data.get('password1')!=form.cleaned_data.get('password2'):
                messages.error(request, 'Enter a Matching Password')
                return redirect('MAIN:register')

            # Check if the email is already registered
            if email and User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
                return redirect('MAIN:register')

            # Check if the phone number is already registered
            if phone and UserProfile.objects.filter(phone=phone).exists():
                messages.error(request, 'Phone number is already registered')
                return redirect('MAIN:register')

            # Set the password manually using set_password to hash it
            user.set_password(password)

            # Save the user object
            user.save()

            # If a phone number was provided, create or update the user profile
            if phone:
                # Use `get_or_create` to avoid issues with non-existent profiles
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.phone = phone
                profile.save()

            messages.success(request, 'Your account has been created successfully!')
            return redirect('MAIN:login')  # Redirect to login page after successful registration

        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    # If the user is already authenticated, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('MAIN:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to the home page or dashboard after successful login
                return redirect('MAIN:index')
            else:
                # Invalid username or password
                messages.error(request, "Invalid username or password.")
        else:
            # Form validation errors (e.g., missing fields, incorrect input)
            for field in form.errors:
                messages.error(request, f"Error with field '{field}': {form.errors[field][0]}")
    
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    # Log out the user
    logout(request)
    
    # Redirect to the homepage or login page after logout
    return redirect('MAIN:index')

def generate_gst_bill(request, order_id):
    # Retrieve the order object
    order = Order.objects.get(id=order_id)

    # Optionally, you can pass GSTIN and Company Name from settings or hard-code them
    company_name = "Your Printing Company"
    gstin = "123456789012345"

    # Render the HTML template
    html_string = render_to_string('gst_bill.html', {
        'order': order,
        'company_name': company_name,
        'gstin': gstin
    })

    # Generate PDF using WeasyPrint
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Send the PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="GST_Bill_{order.id}.pdf"'
    return response

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.all()
    return render(request, 'product_detail.html', {'product': product,'products': products})

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html' ,{'products': products})

def about(request):
    products = Category.objects.all()
    return render(request, 'about.html',{'products': products})
def order(request):
    return render(request, 'booking.html')



def contact(request):
    success_message = None

    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        number_of_prints = request.POST.get('number_of_prints')
        delivery_date = request.POST.get('delivery_date')
        address = request.POST.get('address')
        product = request.POST.get('product')
        delivery_location = request.POST.get('delivery_location')

        # Simple form validation (you can add more validation as needed)
        if not name or not phone_number or not number_of_prints or not delivery_date or not address or not product or not delivery_location:
            return HttpResponse("All fields are required.", status=400)

        # Save the data in the Contact model
        contact = Contact(
            name=name,
            phone_number=phone_number,
            number_of_prints=number_of_prints,
            delivery_date=delivery_date,
            address=address,
            product=product,
            delivery_location=delivery_location
        )
        contact.save()

        # Display a success message
        success_message = "Your contact request has been submitted successfully!"
        
        # After successful submission, you could either redirect or just clear the form
        return render(request, 'contact.html', {'success_message': success_message})
    
    return render(request, 'contact.html', {'success_message': success_message})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:  # If the item already exists, update the quantity
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')



@login_required
def cart_view(request):
    # Get the user's cart (or create it if it doesn't exist)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    # Calculate total price
    total_price = cart.get_total_price()
    
    # Pass the cart and total price to the template
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def update_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        # Check if quantity is valid (not more than stock)
        if 1 <= quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            # Handle invalid quantity, maybe add a message for the user
            pass
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
