from users import views
from django.urls import path


urlpatterns = [
    path('admin/', views.signup , name = 'signup'),
    path('cashier/', views.signup, name = 'signup'),
    path('user/', views.signup, name = 'signup'),
    path('user/login',views.login, name = 'login'),
    path('admin/login', views.login, name = 'login'),
    path('cashier/login', views.login, name = 'login')
]


#auth/user/login