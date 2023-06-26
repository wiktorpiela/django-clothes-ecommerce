from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages

def home(request):
    products = Product.objects.filter(is_available=True)
    return render(request, "home.html", {"products":products})

def store(request, categorySlug=None):
    categories = None
    products = None

    if categorySlug != None:
        categories = get_object_or_404(Category, slug=categorySlug)
        products = Product.objects.filter(category=categories, is_available=True).order_by("id")
    else:
        products = Product.objects.filter(is_available=True).order_by("id")
        
    prodCount = products.count()
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "products":paged_products,
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

def search(request):
    keywords = request.POST.get("keyword").split(" ")
    
    for keyword in keywords:
        
        products = Product.objects.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(slug__icontains=keyword)
            )
        try:
            questions = questions | products
        except UnboundLocalError:
            questions = products

    productsCount = questions.count()
    questions = list(set(questions.order_by("-created_date")))
         
    context = {
        "products":questions,
        "prodCount":productsCount
    }

    return render(request, "store/store.html", context)

def submit_review(request, productID):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id,
                                               product__id = productID)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you! Your review has been updated!")
                return redirect(url)
            else:
                messages.error(request, "Something went wrong, please try again!")
                return redirect("store:submit_review")

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = productID
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted!")
                return redirect(url)

