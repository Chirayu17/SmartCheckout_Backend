from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import AdminTokenAuthentication, AdminPermission
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
# Create your views here.



class ProductView(APIView):
    @authentication_classes(AdminTokenAuthentication)
    @permission_classes(AdminPermission)

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

    def get(self, request, category_name = None, subCategory_name = None):
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
        
        elif subCategory_name is not None:
            try:
                product = Product.objects.filter(categories = subCategory_name)
                if not product:
                    error_message = "No product found."
                    return JsonResponse({'error': error_message}, status=404)
                
                product_serializer = ProductSerializer(product, many = True)
                data = product_serializer.data
                return JsonResponse(data, content_type='application/json', status=200, safe=False)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)

        
    
    def post(self, request, category_name = None, subCategory_name = None):
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
        
        elif subCategory_name is not None:
            print("subcategory name->", subCategory_name)
            request_data = json.loads(request.body)
            try:
                subcategory = Category.objects.get(name = subCategory_name)
                if not subcategory:
                    error_message = "No categories found."
                    return JsonResponse({'error': error_message}, status=404)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'error': error_message}, status=500)
            
            # print("type of image before ->", type(request_data["image"]))
            
            try:
                image_data = base64.b64decode(request_data["image"])
            except binascii.Error:
                return HttpResponseBadRequest("Invalid base64 image")
            
            if not image_data:
                    return HttpResponseBadRequest("Empty decoded image data")
            # print("image_data->", image_data)
            # img_file = open('Grapefruit.jpeg', 'wb')
            # img_file.write(image_data)
            # img_file.close()
            # print("type of image->", type(image_data))

            image_stream = io.BytesIO(image_data)
            image_binary = image_stream.getvalue()


            product_data = {"name": request_data["name"], "created_at": datetime.datetime.now(), "modified_at": datetime.datetime.now(), "price" : request_data["price"], "quantity" : request_data["quantity"], "isActive": request_data["isActive"], "image" : base64.b64encode(image_binary).decode("utf-8"),  "categories": [subcategory]}
            serializer = ProductSerializer(data = product_data)
            if serializer.is_valid():
                product_instance=serializer.save()
                data = serial.serialize('json', [product_instance,])
            else:
                return JsonResponse({'error': serializer.errors})
            return JsonResponse({"data" : data})

        return JsonResponse({"data" : data})
    
    
    def put(self, request, category_name = None, product_name = None):
        data = {}
        if category_name is not None:
            try:
                category_instance = Category.objects.get(name=category_name)
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
       
    
        elif product_name is not None:
            try:
                product_instance = Product.objects.get(name=product_name)
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
                    image_data = base64.b64decode(request_data["image"])
                    if not image_data:
                        return HttpResponseBadRequest("Empty decoded image data")
                    else:
                        product_data['image'] = image_data
                except binascii.Error:
                    return HttpResponseBadRequest("Invalid base64 image")
                image_stream = io.BytesIO(image_data)
                image_binary = image_stream.getvalue()

                product_data["image"] = base64.b64encode(image_binary).decode("utf-8")

            
            product_data['modified_at'] = datetime.datetime.now()

            serializer = ProductSerializer(instance= product_instance, data= product_data, partial=True)
            if serializer.is_valid():
                product_instance = serializer.save()
                data = serial.serialize('json', [product_instance,])
                return JsonResponse({"data": data})
            else:
                return JsonResponse({'error': serializer.errors}, status=400)

        return JsonResponse({"data" : data}, status = 200)


        