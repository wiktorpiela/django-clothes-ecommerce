from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("store-page/", views.store, name="store"),
    path("store-page/<slug:categorySlug>/", views.store, name="products_by_category"),
]