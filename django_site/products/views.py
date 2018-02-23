from django.http import HttpResponse          
from django.views import generic 
from .models import Product
from .models import Category
  
def index(request): 
    return HttpResponse("Hello, world. You're at the products index.")

class IndexView(generic.ListView): 
    template_name = 'products_list.html'
    context_object_name = 'products'
    model = Product

class ProductDetail(generic.DetailView): 
    template_name = 'product_detail.html' 
    model = Product

class Category(generic.DetailView):
    template_name = 'products_category.html'
    model = Category