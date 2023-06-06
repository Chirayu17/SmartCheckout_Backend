from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('category', views.ProductView.as_view(), name = 'category'),
    path('<str:category_name>',views.ProductView.as_view(), name = 'category'),
    path('products/<str:product_name>', views.ProductView.as_view(), name = 'category')
]