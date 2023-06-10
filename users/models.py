from django.db import models


class Cashier(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=255,null = False)
    phoneNumber = models.CharField(max_length = 10,unique= True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=256,null = False, unique= True)
    password = models.CharField(max_length=256,null = False)
    isActive = models.BooleanField(null= False, default=True)



#retail user
class User(models.Model):
    name = models.CharField(max_length=255,null = False)
    phoneNumber = models.CharField(max_length = 10,unique= True, primary_key= True)
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.CharField(max_length=255,null = False)
    isActive = models.BooleanField(null= False, default=True)

#access to inventory
class admin_user(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=255,null = False)
    phoneNumber = models.CharField(max_length = 10,unique= True)
    created_at = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(null= False, default=True)
    email = models.CharField(max_length=256,null = False, unique= True)
    password = models.CharField(max_length=256,null = False)
    