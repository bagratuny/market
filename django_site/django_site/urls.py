# стандартный вью для админки
from django.contrib import admin
# модуль Джанго для определения урлов
from django.urls import path 
# импортируем наш файл views из products
from products import views 
from django.conf.urls.static import static
from django.conf import settings

# говорим Джанго о том, что хотим отображать наш вью на главной странице
# а строчкой ниже, кстати ссылка на нашу админку, про нее позже
urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'), 
    path('admin/', admin.site.urls),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='detail'),
    path('category/<slug:slug>/', views.Category.as_view(), name='category')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)