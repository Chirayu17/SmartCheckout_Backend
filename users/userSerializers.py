from users.models import admin_user, User, Cashier
from rest_framework import serializers


class admin_userSerializer(serializers.ModelSerializer):
    class Meta : 
        model = admin_user
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta : 
        model = User
        fields = '__all__'


class CashierSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Cashier
        fields = '__all__'
