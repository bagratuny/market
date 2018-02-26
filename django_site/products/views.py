from django.http import HttpResponse          
from django.views import generic 
from .models import Product
from .models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests

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
        context['objects'] = Product.objects.filter(category__slug = self.kwargs['slug'])
        context['categorys'] = Category.objects.all()

        paginator = Paginator(context['objects'], 6)
        page = self.request.GET.get('page', 1)
        context['products'] = paginator.get_page(page)

        return context

