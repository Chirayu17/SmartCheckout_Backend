from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import TokenAuthentication, AuthorPermission
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from inventory.models import Category, Product
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import  authentication_classes,permission_classes
from inventory.productSerializers import ProductSerializer, CategorySerializer
import keys
from django.core import serializers as serial
import datetime
import base64
import binascii
# Create your views here.



class ProductView(APIView):
    @authentication_classes(TokenAuthentication)


    def get(self, request, category_name = None, product_name = None):
        if request.path == '/inventory/category':
            try:
                categories = Category.objects.all()
                if not categories:
                    error_message = "No categories found."
                    return JsonResponse({'error': error_message}, status=404)
                
                category_serializer = CategorySerializer(categories, many=True)
                data = category_serializer.data
                return JsonResponse(data, content_type='application/json', status=200, safe=False)

            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)

        
        elif category_name is not None:
            try:
                category = Category.objects.filter(parent_category =category_name)
                if not category:
                    error_message = "No categories found."
                    return JsonResponse({'error': error_message}, status=404)
                
                category_serializer = CategorySerializer(category, many = True)
                data = category_serializer.data
                return JsonResponse(data, content_type='application/json', status=200, safe=False)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)
        
        elif product_name is not None:
            try:
                product = Product.objects.filter(categories = product_name)
                if not product:
                    error_message = "No categories found."
                    return JsonResponse({'error': error_message}, status=404)
                
                product_serializer = ProductSerializer(product, many = True)
                data = product_serializer.data
                return JsonResponse(data, content_type='application/json', status=200, safe=False)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)

        

    def post(self, request, category_name = None, product_name = None):
        data = {}
        if request.path == '/inventory/category':
            request_data = json.loads(request.body)
            category_data = {"name" : request_data["name"], "created_at": datetime.datetime.now(), "modified_at": datetime.datetime.now(), "isActive" :request_data["isActive"] }
            
            serializer = CategorySerializer(data = category_data)
            if serializer.is_valid():
                category_instance=serializer.save()
                data = serial.serialize('json', [category_instance,])
            else:
                return JsonResponse({'error': serializer.error})
            return JsonResponse({"data" : data})
        
        elif category_name is not None:

            request_data = json.loads(request.body)
            category = Category.objects.get(name = category_name)
            print(category)
            subcategory_data = {"name" : request_data["name"], "created_at": datetime.datetime.now(), "modified_at": datetime.datetime.now(), "isActive" : request_data["isActive"], "parent_category" : category}
            
            serializer = CategorySerializer(data = subcategory_data)
            if serializer.is_valid():
                category_instance=serializer.save()
                data = serial.serialize('json', [category_instance,])
            else:
                return JsonResponse({'error': serializer.error})
            return JsonResponse({"data" : data})
        
        elif product_name is not None:
            request_data = json.loads(request.body)
            subcategory = Category.objects.get(name = product_name)

            try:
                image_data = base64.b64decode(request_data["image"])
            except binascii.Error:
            # Handle invalid base64 encoding
                return HttpResponseBadRequest("Invalid base64 image")
            
            if not image_data:
                    return HttpResponseBadRequest("Empty decoded image data")
            print("image_data->", image_data)

            product_data = {"name": request_data["name"], "created_at": datetime.datetime.now(), "modified_at": datetime.datetime.now(), "price" : request_data["price"], "quantity" : request_data["quantity"], "isActive": request_data["isActive"], "image" : image_data,   "categories": [subcategory]}
            serializer = ProductSerializer(data = product_data)
            if serializer.is_valid():
                product_instance=serializer.save()
                data = serial.serialize('json', [product_instance,])
            else:
                return JsonResponse({'error': serializer.errors})
            return JsonResponse({"data" : data})

        return JsonResponse({"data" : data})

        