from inventory.models import Category, Product
from rest_framework import serializers
import base64


class CategorySerializer(serializers.ModelSerializer):
    class Meta : 
        model = Category
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        print("obj->", obj)
        if obj.image:
            base64_image = base64.b64encode(obj.image).decode('utf-8')
            return base64_image
        else:
            return 'Empty Image'
    class Meta : 
        model = Product
        fields = '__all__'

