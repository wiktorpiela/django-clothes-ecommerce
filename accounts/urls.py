from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("user-login/", views.user_login, name="user_login"),
    path("user-logout/", views.user_logout, name="user_logout"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("", views.dashboard, name="dashboard"),

    
]