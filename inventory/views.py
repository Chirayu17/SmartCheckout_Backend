from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import TokenAuthentication, Permission
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from inventory.models import Category, Product
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import  authentication_classes,permission_classes
from inventory.productSerializers import ProductSerializer, CategorySerializer
from django.core import serializers as serial
import datetime
import base64
import binascii
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import io
import psycopg2
# Create your views here.



class ProductView(APIView):
    @authentication_classes(TokenAuthentication)
    @permission_classes(Permission)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='category_name',
                in_=openapi.IN_QUERY,
                description='Filter by category name',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='subCategory_name',
                in_=openapi.IN_QUERY,
                description='Filter by subcategory name',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description='OK',
                schema=CategorySerializer(many=True)
            ),
            404: 'Not Found',
            500: 'Internal Server Error'
        }
    )

    def get(self, request, categoryName = None, subCategoryName = None):
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

        
        elif categoryName is not None:
            try:
                category = Category.objects.filter(parent_category =categoryName)
                if not category:
                    error_message = "No categories found."
                    return JsonResponse({'error': error_message}, status=404)
                
                category_serializer = CategorySerializer(category, many = True)
                data = category_serializer.data
                return JsonResponse(data, content_type='application/json', status=200, safe=False)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)
        
        elif subCategoryName is not None:
            try:
                product = Product.objects.filter(categories = subCategoryName)
                if not product:
                    error_message = "No product found."
                    return JsonResponse({'error': error_message}, status=404)
                
                product_serializer = ProductSerializer(product, many = True)
                data = product_serializer.data
                return JsonResponse(data, content_type='application/json', status=200, safe=False)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)

        
    
    def post(self, request, categoryName = None, subCategoryName = None):
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
        
        elif categoryName is not None:

            request_data = json.loads(request.body)
            category = Category.objects.get(name = categoryName)
            print(category)
            subcategory_data = {"name" : request_data["name"], "created_at": datetime.datetime.now(), "modified_at": datetime.datetime.now(), "isActive" : request_data["isActive"], "parent_category" : category}
            
            serializer = CategorySerializer(data = subcategory_data)
            if serializer.is_valid():
                category_instance=serializer.save()
                data = serial.serialize('json', [category_instance,])
            else:
                return JsonResponse({'error': serializer.error})
            return JsonResponse({"data" : data})
        
        elif subCategoryName is not None:
            print("subcategory name->", subCategoryName)
            request_data = json.loads(request.body)
            try:
                subcategory = Category.objects.get(name = subCategoryName)
                if not subcategory:
                    error_message = "No categories found."
                    return JsonResponse({'error': error_message}, status=404)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)
            
            # print("type of image before ->", type(request_data["image"]))
            
            # try:
            #     image_data = base64.b64decode(request_data["image"])
            # except binascii.Error:
            #     return JsonResponse({"error" : "Invalid base64 image"}, status = 500)
            
            # if not image_data:
            #         return JsonResponse({"error" : "Empty decoded image data"}, status = 500)
         


            product_data = {"name": request_data["name"], "created_at": datetime.datetime.now(), "modified_at": datetime.datetime.now(), "price" : request_data["price"], "quantity" : request_data["quantity"], "isActive": request_data["isActive"], "image" : request_data["image"],  "categories": [subcategory]}
            serializer = ProductSerializer(data = product_data)
            if serializer.is_valid():
                product_instance=serializer.save()
                data = serial.serialize('json', [product_instance,])
            else:
                return JsonResponse({'error': serializer.errors})
            return JsonResponse({"data" : data})

        return JsonResponse({"data" : data})
    
    
    def put(self, request, categoryName = None, productName = None):
        data = {}
        if categoryName is not None:
            try:
                category_instance = Category.objects.get(name=categoryName)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found.'}, status=404)

            request_data = json.loads(request.body)
            category_data = {}

            if 'name' in request_data:
                category_data['name'] = request_data['name']

            if 'isActive' in request_data:
                category_data['isActive'] = request_data['isActive']

            category_data['modified_at'] = datetime.datetime.now()

            serializer = CategorySerializer(instance=category_instance, data=category_data, partial=True)
            if serializer.is_valid():
                category_instance = serializer.save()
                data = serial.serialize('json', [category_instance,])
                return JsonResponse({"data": data})
            else:
                return JsonResponse({'error': serializer.errors}, status=400)
       
    
        elif productName is not None:
            try:
                product_instance = Product.objects.get(name=productName)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found.'}, status=404)
            
            request_data = json.loads(request.body)
            product_data = {}
            if 'name' in request_data:
                product_data['name'] = request_data['name']

            if 'isActive' in request_data:
                product_data['isActive'] = request_data['isActive']
            if 'quantity' in request_data:
                product_data['quantity'] = request_data['quantity']
            if 'price' in request_data:
                product_data['price'] = request_data['price']
                

            if 'image' in request_data:
                try:
                    product_data["image"] = request_data["image"]
                except binascii.Error:
                    return JsonResponse({"error" : "Invalid base64 image"}, status = 500)
            
                # if not image_data:
                #     return JsonResponse({"error" : "Empty decoded image data"}, status = 500)
                
      
                # product_data["image"] = psycopg2.Binary(image_data)
            # print(product_data["image"])
            product_data['modified_at'] = datetime.datetime.now()
            print("product_data ->", product_data)
            # try:
            #     Product.objects.filter(name=productName).update(modified_at=product_data['modified_at'], image = product_data["image"])
            # except Exception as e:
            #     return JsonResponse({"error" : e}, status = 500)
            
            # try:
            #     updated_instance = Product.objects.get(name=productName)
            # except Exception as e:
            #     return JsonResponse({"error" : e}, status = 500)

            # # Check if the instance has been updated
            # if updated_instance.modified_at == product_data['modified_at'] and updated_instance.image == product_data["image"]:
            #     print("Instance has been successfully updated!")
            # else:
            #     print("Instance update failed!")

            serializer = ProductSerializer(instance= product_instance, data= product_data, partial=True)
            if serializer.is_valid():
                print("serialized_data->", serializer.validated_data)
                if serializer.is_valid():
                    product_instance = serializer.save()
                data = serial.serialize('json', [product_instance,])
                jsonData = json.loads(data)
                return JsonResponse({"data": jsonData})
            else:
                return JsonResponse({'error': serializer.errors}, status=400)

        return JsonResponse({"data" : data}, status = 200)


        