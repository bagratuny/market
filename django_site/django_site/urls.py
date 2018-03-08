from django.contrib import admin
from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings
from products import views 
from django.urls import path, include
from django.views.decorators.http import require_POST

urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'), 
    path('admin/', admin.site.urls),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('product/create', views.NewProduct.as_view(), name='product_create'),
    path('product/<slug:slug>/order', views.Order.as_view(), name='product_order'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('login', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)