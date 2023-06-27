from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.CartView.as_view(), name = 'orders'),
    path('<int:orderID>', views.CartView.as_view(), name = 'orders'),
    path('<int:orderID>/<int:orderItemID>', views.CartView.as_view(), name = 'orders'),
    path('orderItems/<int:orderID>', views.CartView.as_view(), name = 'orders'),
    path('addNew/', views.CartView.as_view(), name = 'orders'),
    path('addNew/<int:orderID>', views.CartView.as_view(), name = 'orders')
]