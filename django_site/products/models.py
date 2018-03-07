from django.db import models
from djmoney.models.fields import MoneyField
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Product(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey('Category', on_delete='CASCADE', null=True, related_name='products')
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)
    image = models.ImageField(upload_to = '', default = 'pic_folder/none.jpg', blank=True)
    slug = models.SlugField(max_length=50, default=title)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self): 
        return reverse('detail', args=[str(self.slug)])

class Category(models.Model): 
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, default=None)

    def __str__(self):
        return self.title

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete="CASCADE")
    customer_name = models.CharField(max_length=50)
    customer_phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete="CASCADE", blank=True, null=True)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete="CASCADE", blank=False, null=False)
    user = models.ForeignKey(User, on_delete="CASCADE", blank=True, null=True)
    content = models.TextField(max_length=5000)
    created_date = models.DateTimeField(auto_now_add=True)
