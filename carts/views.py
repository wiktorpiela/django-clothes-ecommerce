from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = 23*total/100
        grand_total = total+tax
    except Cart.DoesNotExist:
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
    product = Product.objects.get(pk=productID)
    product_variation = []
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product = product, 
                                                  variation_category__iexact = key, 
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #get cart using the cart_id in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    cart.save()

    cartItemExists = CartItem.objects.filter(product=product, cart=cart).exists()

    if cartItemExists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        ids = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            ids.append(item.id)

        if product_variation in ex_var_list:
            #increase cart item quantity
            index = ex_var_list.index(product_variation)
            itemId = ids[index]
            item = CartItem.objects.get(product=product, id=itemId)
            item.quantity += 1
            item.save()

        else:
            #create new cart item
            item = CartItem.objects.create(product=product, quantity = 1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()

    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
        
    return redirect("carts:cart")

def remove_cart(request, productID, actionLocation, cartItemID):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=productID)

    cart_item = CartItem.objects.get(product=product, cart=cart, pk = cartItemID)

    if actionLocation=="decrement":

        if cart_item.quantity>1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    else:
        cart_item.delete()

    return redirect("carts:cart")

@login_required
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = 23*total/100
        grand_total = total+tax
    except Cart.DoesNotExist:
        pass

    context = {
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "tax":tax,
        "grand_total":grand_total
        }

    return render(request, "store/checkout.html", context)



    


