from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('addNew/', views.OrderView.as_view(), name = 'orders'),
    path('addNew/<int:orderID>', views.OrderView.as_view(), name = 'orders')
]