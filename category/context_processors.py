from .models import Category

def get_category_links(request):
    links = Category.objects.all()
    return dict(links=links)