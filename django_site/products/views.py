from django.http import HttpResponse
# импортируем модель для CBV            
from django.views import generic 
# импортируем нашу модель
from .models import Product
from .models import Category
  
# Стандартный вью — это обычная питон-функция
def index(request): 
    return HttpResponse("Hello, world. You're at the products index.")

class IndexView(generic.ListView): 
    template_name = 'products_list.html' # подключаем наш Темплейт
    context_object_name = 'products' # под каким именем передадутся данные в Темплейт
    model = Product # название Модели

class ProductDetail(generic.DetailView): 
    template_name = 'product_detail.html' 
    model = Product

class Category(generic.DetailView):
    template_name = 'products_category.html'
    model = Category