from .models import Cart, CartItem, Order, UserProfile
from .forms import CustomLoginForm, RegisterForm
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

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Get the form data
            user = form.save(commit=False)  # Don't save the user immediately
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')

            # Check if the username already exists
            if username and User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('MAIN:register')

            # Check if the email is already registered
            if email and User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
                return redirect('MAIN:register')

            # Check if the phone number is already registered
            if phone and UserProfile.objects.filter(phone=phone).exists():
                messages.error(request, 'Phone number is already registered')
                return redirect('MAIN:register')

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


def index(request):
    return render(request, 'index.html')

def about(request):
    products = Product.objects.all()
    return render(request, 'about.html',{'products': products})
def order(request):
    return render(request, 'booking.html')

def pricing(request):
    return render(request, 'pricing.html')
def contact(request):
    return render(request, 'contact.html')



@login_required
def cart_view(request):
    # Ensure the cart exists for the user
    cart, created = Cart.objects.get_or_create(customer=request.user)

    context = {
        'cart': cart
    }
    return render(request, 'cart/cart_page.html', context)

@login_required
def update_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    
    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart:view')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()

    return redirect('cart:view')
