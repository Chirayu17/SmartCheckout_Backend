from inventory.models import Category, Product
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
import psycopg2
import base64

class CategorySerializer(serializers.ModelSerializer):
    class Meta : 
        model = Category
        fields = '__all__'

# class BinaryField(serializers.Field):
#     def to_representation(self, value):
#         return value

#     def to_internal_value(self, data):
#         return base64.b64encode(data).decode('utf-8')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'



