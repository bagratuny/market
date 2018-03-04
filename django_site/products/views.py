from django.http import HttpResponse          
from django.views import generic 
from .models import Product
from .models import Category
from .models import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy 
from django.contrib.auth.forms import UserCreationForm 
import requests
from django.contrib.auth import get_user_model
from django.conf import settings


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

class NewProduct(generic.CreateView):
    template_name = 'create.html'
    model = Product
    fields = '__all__'

class Order(generic.CreateView):
    model = Order
    template_name = 'order.html'
    success_url = '/'
    fields = ['customer_name', 'customer_phone_number']

    def form_valid(self, form):
        user = self.request.user 
        if user.is_authenticated:
            form.instance.user = user
        product = Product.objects.get(slug=self.kwargs['slug']) 
        form.instance.product = product 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.filter(slug = self.kwargs['slug'])
        context['order'] = context['product'].get()
        return context

class Signup(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')