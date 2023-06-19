from django.db import models
from orders.models import Orders
from users.models import User
# Create your models here.

class Payments(models.Model):
    orderID = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits= 10, decimal_places= 2)
    razorpay_payment_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
