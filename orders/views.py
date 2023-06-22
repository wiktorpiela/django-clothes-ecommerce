from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from datetime import datetime
import json
from store.models import Product

def place_order(request, total=0, quantity=0):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect("store:home")
    
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = round(23*total/100,2)
    grand_total = total+tax
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            #populating model with billing information
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]

            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            #generating order number
            current_date = datetime.now().strftime("%Y%m%d%H%M%S")
            order_number = f"{current_date}_{data.id}"
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=request.user, is_ordered = False, order_number = order_number)
            context = {
                "order":order,
                "cart_items":cart_items,
                "total":total,
                "tax":tax,
                "grand_total":grand_total,
            }
            return render(request, "orders/payments.html", context)
        else:
            return HttpResponse("something wrong")  
    else:
        return redirect("carts:checkout")
    
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body["orderID"])
    #Store trans details in paymnts model
    payment = Payment(
        user = request.user,
        payment_id = body["transID"],
        payment_method = body["payment_method"],
        amount_paid = order.order_total,
        status = body["status"],
    )
    payment.save()
    order.is_ordered = True
    order.payment = payment
    order.save()

    #move the cart items to order product table
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        #reduce quantity of sold products in stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #clear the cart
    CartItem.objects.filter(user=request.user).delete()

    #send confirmation mail to customer

    #send order number and transaction id back to  sendData methon by response

    return render(request, "orders/payments.html")

        
