from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
def order(request):
    return render(request, 'booking.html')

def pricing(request):
    return render(request, 'pricing.html')
def contact(request):
    return render(request, 'contact.html')