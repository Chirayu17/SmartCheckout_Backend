from payments import views
from django.urls import path


urlpatterns = [
    path('addNew/', views.PaymentView.as_view() , name = 'payments'),
]
