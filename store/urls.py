from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("store-page/", views.store, name="store"),
    path("store-page/category/<slug:categorySlug>/", views.store, name="products_by_category"),
    path("store-page/<slug:categorySlug>/<slug:productSlug>/", views.product_details, name="product_details"),
    path("search/", views.search, name="search"),
    path("submit-review/<int:productID>/", views.submit_review, name="submit_review"),
]