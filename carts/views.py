from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = 23*total/100
        grand_total = total+tax
    except CartItem.DoesNotExist:
        pass

    context = {
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "tax":tax,
        "grand_total":grand_total
        }
    
    return render(request, "store/cart.html", context)

def add_cart(request, productID):
    color = request.GET["color"]
    size = request.GET["size"]

    return HttpResponse(f"{color} {size}")
    exit()

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

def remove_cart(request, productID, actionLocation):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=productID)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if actionLocation=="decrement":

        if cart_item.quantity>1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    else:
        cart_item.delete()

    return redirect("carts:cart")



    


