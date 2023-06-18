from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
            messages.success(request, "Account has been created.")
            return redirect("accounts:register")

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
                    return redirect("store:home")
                else:
                    messages.error(request, "Invalid credentials. Try again!")
                    return redirect("accounts:user_login")

    return render(request, "accounts/user_login.html")

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("accounts:user_login")
