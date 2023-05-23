from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request):
    return render(request, "store/cart.html")

def add_cart(request, productID):
    product = Product.objects.get(pk=productID)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #get cart using the cart_id in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
        
    return redirect("carts:cart")
    


