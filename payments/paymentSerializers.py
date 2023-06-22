from payments.models import Payments
from rest_framework import serializers
import base64


class PaymentSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Payments
        fields = '__all__'
