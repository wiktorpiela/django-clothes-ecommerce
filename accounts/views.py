from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse

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
            currentSite = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string("accounts/account_verification_email.html", {
                "user": user,
                "domain": currentSite,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user)
            })

            emailReceiver = email
            send_email= EmailMessage(mail_subject, 
                                     message, 
                                     to=[emailReceiver])
            send_email.send()
    
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
                    login(request, user)
                    messages.success(request, "Logged in successfully.")
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
    return render(request, "accounts/dashboard.html")



