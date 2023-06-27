from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, ResetPasswordForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .func import send_custom_email
from django.http import HttpResponse
from carts.models import Cart, CartItem
from carts.views import _cart_id
import requests
from orders.models import Order

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username
            )

            user.phone_number = phone_number
            user.save()

            #user activation
            send_custom_email(request, 
                              "Please activate your account", 
                              "accounts/account_verification_email.html",
                              user,
                              email)
    
            # messages.success(request, f"Account has been created. Check your mail {email} to activate this account.")
            return redirect("/accounts/user-login/?command=verification&email="+email)
        
    else:
        form = RegistrationForm()
        
    context = {
        "form":form
    }
    return render(request, "accounts/register.html", context)

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        userExists = Account.objects.filter(email=email).exists()

        if not userExists:
            messages.error(request, "This user does not exist.")
            return redirect("accounts:user_login")
        
        else:
            userIsActive = Account.objects.filter(email=email, is_active=True).exists()

            if not userIsActive:
                messages.error(request, "This user is inactive. Activate your account, then try again.")
                return redirect("accounts:user_login")
            
            else:
                user = authenticate(username=email, password=password)

                if user is not None:
                    try:
                        cart = Cart.objects.get(cart_id= _cart_id(request))
                        cartItemExists = CartItem.objects.filter(cart=cart).exists()
                        if cartItemExists:
                            cart_item = CartItem.objects.filter(cart=cart)

                            #getting product variation by cart id
                            product_variation = []
                            for item in cart_item:
                                variation = item.variations.all()
                                product_variation.append(list(variation))

                            #getting cart items from user to access his product variation
                            cart_item = CartItem.objects.filter(user=user)
                            ex_var_list = []
                            ids = []
                            for item in cart_item:
                                existing_variation = item.variations.all()
                                ex_var_list.append(list(existing_variation))
                                ids.append(item.id)

                            for pr in product_variation:
                                if pr in ex_var_list:
                                    index = ex_var_list.index(pr)
                                    item_id = ids[index]
                                    item = CartItem.objects.get(id=item_id)
                                    item.quantity +=1
                                    item.user = user
                                    item.save()
                                
                                else:
                                    cart_item = CartItem.objects.filter(cart=cart)
                                    for item in cart_item:
                                        item.user = user
                                        item.save()

                    except:
                        pass

                    login(request, user)
                    messages.success(request, "Logged in successfully.")
                    url = request.META.get("HTTP_REFERER")
                    try:
                        query = requests.utils.urlparse(url).query
                        #next=/cart/checkout/
                        params = dict(x.split("=") for x in query.split("&"))
                        if "next" in params:
                            nextPage = params["next"]
                            return redirect(nextPage)
                    except:
                        return redirect("accounts:dashboard")
                else:
                    messages.error(request, "Invalid credentials. Try again!")
                    return redirect("accounts:user_login")

    return render(request, "accounts/user_login.html")

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("accounts:user_login")

def activate(request, uidb64, token): 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account was actived.")
        return redirect("accounts:user_login")
    else:
        messages.error(request, "Invalid activation link.")
        return redirect("accounts:register")

@login_required  
def dashboard(request):
    orders = Order.objects.order_by("-created_at").filter(user_id = request.user.id, is_ordered=True)
    orders_count = orders.count()
    context = {
        "orders_count": orders_count,

    }
    return render(request, "accounts/dashboard.html", context)

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Account.objects.filter(email=email).exists():
            user = get_object_or_404(Account, email__exact=email)

            #reset_password email
            send_custom_email(request, 
                              "Reset your password", 
                              "accounts/reset_password_email.html",
                              user,
                              email)

            messages.success(request, "Password reset email has been sent to your mailbox.")
            return redirect("accounts:user_login")
        
        else:
            messages.error(request, "Account does not exists.")
            return redirect("account:forgot_password")
        
    return render(request, "accounts/forgot_password.html")

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Reset your password.")
        return redirect("accounts:reset_password")
    else:
        messages.success(request, "This link has been expired. Try again.")
        return redirect("accounts:forgot_password")

def reset_password(request):  
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        password = request.POST.get("password")

        if form.is_valid():
            uid = request.session.get("uid")
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfull.")
            return redirect("accounts:user_login")

    else:
        form = ResetPasswordForm()

    context = {
        "form":form
    }

    return render(request, "accounts/reset_password.html", context)

    




