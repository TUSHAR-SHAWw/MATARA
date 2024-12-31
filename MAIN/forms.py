# main/forms.py
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class ProductSearchForm(forms.Form):
    # Get categories from the database
    category_choices = [(category.id, category.name) for category in Category.objects.all()]
    
    CATEGORY_CHOICES = [('','Select Category')] + category_choices
    
    PRICE_CHOICES = [
        ('100', '₹100 - ₹250'),
        ('250', '₹250 - ₹500'),
        ('500', '₹500 - ₹1,000'),
        ('1000', '₹1,000 - ₹2,500'),
        ('2500+', '₹2,500+'),
    ]
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    price = forms.ChoiceField(choices=PRICE_CHOICES, required=False)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'number_of_prints', 'delivery_date', 'address', 'product', 'delivery_location']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'}))

# In forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and UserProfile.objects.filter(phone=phone).exists():
            raise ValidationError("Phone number is already registered")
        return phone

