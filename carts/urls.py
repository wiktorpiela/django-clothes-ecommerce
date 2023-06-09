from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add-cart/<int:productID>/", views.add_cart, name="add_cart"),
    path("remove-cart/<int:productID>/<str:actionLocation>/<int:cartItemID>/", views.remove_cart, name="remove_cart"),
    path("checkout/", views.checkout, name="checkout"),
    
]