from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('add', views.ImageView.as_view(), name = 'images'),
    path('get/<str:name>', views.ImageView.as_view(), name = 'images')
]