from users import views
from django.urls import path


urlpatterns = [
    path('admin_user/', views.signup , name = 'signup'),
    path('cashier/', views.signup, name = 'signup'),
    path('user/', views.signup, name = 'signup'),
    path('loginUser',views.login, name = 'login'),
    path('loginAdmin', views.login, name = 'login'),
    path('loginCashier', views.login, name = 'login')
]