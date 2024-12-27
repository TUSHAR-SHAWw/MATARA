# main/forms.py
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import AuthenticationForm

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

