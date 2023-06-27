from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import TokenAuthentication, Permission
from rest_framework.decorators import  authentication_classes,permission_classes
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from images.models import Images
from images.imageSerializer import ImageSerializer
from django.core import serializers as serial
import json
import base64
from django.core.files.base import ContentFile
# Create your views here.


class ImageView(APIView):
    @authentication_classes(TokenAuthentication)
    @permission_classes(Permission)


    def get(self, request, name = None):

        data = {}
        imageObject = Images.objects.get(name = name)
        image_data = imageObject.image
        encoded_data = base64.b64encode(image_data).decode('utf-8')
        print("base64->", encoded_data)
        imageData = {"base64encoded" : encoded_data}
        # return HttpResponse(image_data, content_type='image/jpeg')
        # print(imageObject)
        # image_serializer = ImageSerializer(imageObject)
    
        # print("data->", image_serializer.data)
        # data = image_serializer.data
        # print(imageObject)
        return JsonResponse({"data" : imageData}, status = 200)


    def post(self, request):
        data = {}
        request_data = json.loads(request.body)
        image_data = base64.decodebytes(request_data["image"].encode())
        image = base64.encodebytes(image_data).decode()
        # image_file = ContentFile(image_data, name=request_data["name"])
        print("here")
        print("data type->", type(image_data))
        imageObject = {"name" : request_data["name"], "image" : image}
        print(imageObject)
        imageserialized  = ImageSerializer(data = imageObject)

  
        if imageserialized.is_valid():
            image_instance=imageserialized.save()
            imageData = serial.serialize('json', [image_instance,])
            
            data["image"] = json.loads(imageData)[0]
        else:
            return JsonResponse({'error': imageserialized.errors})

        return JsonResponse({"data" : data}, status = 200)