from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

def home(request):
    products = Product.objects.filter(is_available=True)
    return render(request, "home.html", {"products":products})

def store(request, categorySlug=None):
    categories = None
    products = None

    if categorySlug != None:
        categories = get_object_or_404(Category, slug=categorySlug)
        products = Product.objects.filter(category=categories, is_available=True)
        prodCount = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        prodCount = products.count()

    context = {
        "products":products,
        "prodCount":prodCount

    }

    return render(request, "store/store.html", context)
