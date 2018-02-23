from django.db import models
from djmoney.models.fields import MoneyField

class Product(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey('Category', on_delete='CASCADE', null=True, related_name='products')
    price = MoneyField(decimal_places=2, default=0, default_currency='USD', max_digits=11,)
    image = models.ImageField(upload_to = '', default = 'pic_folder/none.jpg', blank=True)
    slug = models.SlugField(max_length=50, default=title)

    def __str__(self):
        return self.title

class Category(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, blank=True)
    slug = models.SlugField(max_length=50, default=None)

    def __str__(self):
        return self.title