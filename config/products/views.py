from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Product

class Products_show(ListView):
    model = Product
    template_name = 'base.html'