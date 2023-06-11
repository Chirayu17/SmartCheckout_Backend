from django.db import models
from users.models import User
from inventory.models import Product
# Create your models here.
class Orders(models.Model):
    orderID =  models.BigAutoField(primary_key= True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default =  False)
    total = models.DecimalField(max_digits=10, decimal_places=2)



class OrderItem(models.Model):
    orderID = models.ForeignKey(Orders, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete= models.CASCADE, null = True)
    productName = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    unAvailable = models.BooleanField(default =  False)
    outOfStock = models.BooleanField(default =  False)
    completed = models.BooleanField(default =  False)


