from django.contrib import admin
from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings
from products import views 

urlpatterns = [ 
    path('', views.IndexView.as_view(), name='index'), 
    path('admin/', admin.site.urls),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='detail'),
    path('category/<slug:slug>/', views.Category.as_view(), name='category')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)