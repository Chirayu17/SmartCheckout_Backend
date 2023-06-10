from orders.models import OrderItem, Orders
from rest_framework import serializers
import base64


class OrderSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Orders
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta : 
        model = OrderItem
        fields = '__all__'