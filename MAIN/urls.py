from django.urls import path
from . import views
app_name = 'MAIN'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact/', views.contact, name='contact'),
    path('order/', views.order, name='order'),
    path('about/', views.about, name='about'),
]
