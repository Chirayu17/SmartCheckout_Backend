from inventory.models import Category, Product
from rest_framework import serializers
import base64


class CategorySerializer(serializers.ModelSerializer):
    class Meta : 
        model = Category
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Product
        fields = '__all__'

