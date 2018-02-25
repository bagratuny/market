from django.http import HttpResponse          
from django.views import generic 
from .models import Product
from .models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(generic.ListView): 
    template_name = 'products_list.html'
    context_object_name = 'products'
    model = Product

    paginate_by = 6
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = Category.objects.all()
        return context

class ProductDetail(generic.DetailView): 
    template_name = 'product_detail.html' 
    model = Product

class CategoryView(generic.DetailView):
    template_name = 'products_category.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = Category.objects.all()
        return context