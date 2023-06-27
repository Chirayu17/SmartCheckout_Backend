from images.models import Images
from rest_framework import serializers
import base64


class ImageSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Images
        fields = '__all__'