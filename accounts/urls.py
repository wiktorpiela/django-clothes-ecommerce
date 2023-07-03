from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("user-login/", views.user_login, name="user_login"),
    path("user-logout/", views.user_logout, name="user_logout"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password-validate/<uidb64>/<token>/", views.resetpassword_validate, name="resetpassword_validate"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("order-details/<str:orderID>/", views.order_details, name="order_details"),
    path("remove-account/", views.remove_account, name="remove_account"),
    path("", views.dashboard, name="dashboard"),
]