from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('category', views.ProductView.as_view(), name = 'category'),
    path('<str:categoryName>',views.ProductView.as_view(), name = 'category'),
    path('products', views.ProductView.as_view(), name = 'category'),
    path('products/<str:subCategoryName>', views.ProductView.as_view(), name = 'category'),
    path('updateProducts/<str:productName>', views.ProductView.as_view(), name = 'category'),
]



#category/all