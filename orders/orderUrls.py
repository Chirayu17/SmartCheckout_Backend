from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.OrderView.as_view(), name = 'orders'),
    path('<int:orderID>', views.OrderView.as_view(), name = 'orders'),
    path('orderItems/<int:orderID>', views.OrderView.as_view(), name = 'orders'),
    path('addNew/', views.OrderView.as_view(), name = 'orders'),
    path('addNew/<int:orderID>', views.OrderView.as_view(), name = 'orders')
]