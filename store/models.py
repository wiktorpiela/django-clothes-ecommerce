from django.db import models
from category.models import Category

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to="media/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category="color", is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size", is_active=True)

class Variation(models.Model):

    variation_category_choice = (
        ("color", "color"),
        ("size", "size"),
    )

    objects = VariationManager()

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=20, choices = variation_category_choice)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product.product_name} {self.variation_value}"
    
