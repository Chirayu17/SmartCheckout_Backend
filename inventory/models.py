from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255,null = False, unique= True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(null= False, default=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.TextField(default= "")
    isActive = models.BooleanField(null= False, default=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField('Category')
    probability = models.DecimalField(max_digits=10, decimal_places=2, default = 0)

    def __str__(self):
        return self.name
