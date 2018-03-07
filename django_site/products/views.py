from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic.edit import FormMixin
from django import forms
import requests
from .models import Product
from .models import Category
from .models import Order
from .models import Review

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

class ProductDetail(FormMixin, generic.DetailView):
    template_name = 'product_detail.html'
    model = Product
    form_class = ReviewForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all().filter(product__slug=self.kwargs['slug'])
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        product = Product.objects.get(slug=self.kwargs['slug'])
        form.instance.product = product
        user = self.request.user
        if user.is_authenticated:
            form.instance.user = user
        form.save()
        return super().form_valid(form)

class CategoryView(generic.DetailView):
    template_name = 'products_category.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Product.objects.filter(category__slug=self.kwargs['slug'])
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
        context['product'] = Product.objects.filter(slug=self.kwargs['slug'])
        context['order'] = context['product'].get()
        return context

class Signup(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
