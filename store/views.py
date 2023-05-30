from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id

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

def product_details(request, categorySlug, productSlug):
    try:
        single_product = Product.objects.get(category__slug=categorySlug, 
                                             slug=productSlug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        "single_product":single_product,
        "in_cart":in_cart,
        }
    
    return render(request, "store/product_details.html", context)
