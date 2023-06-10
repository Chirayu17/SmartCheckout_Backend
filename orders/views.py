from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import TokenAuthentication, UserPermission, AdminPermission
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from inventory.models import Category, Product
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import  authentication_classes,permission_classes
from inventory.productSerializers import ProductSerializer, CategorySerializer
from orders.orderSerializer import OrderItemSerializer, OrderSerializer
from django.core import serializers as serial
import datetime
import base64
import binascii
from drf_yasg import openapi
from orders.models import OrderItem, Orders
from users.models import User


class OrderView(APIView):
    @authentication_classes(TokenAuthentication)
    @permission_classes(AdminPermission)


    def post(self, request, orderID = None):
        if orderID is None:
            data = {}
            order_items = []
            total_price = 0
            print("user->",request.user)
            try:
                userObject = User.objects.filter(phoneNumber = request.user)
            except Exception as e:
                        error_message = str(e)
                        return JsonResponse({'error': error_message}, status=500)

            request_data = json.loads(request.body)
            orderObject = {"user" : userObject, "completed" :  False, "created_at" : datetime.datetime.now(), "total" : 0 }
            orderserialized  = OrderSerializer(data = orderObject)
            orderData = {}
            if orderserialized.is_valid():
                order_instance=orderserialized.save()
                orderData = serial.serialize('json', [order_instance,])
            else:
                return JsonResponse({'error': orderserialized.error})
            
            for products in request_data["orderItems"]:
                    productData = {}
                    product_name = request_data["orderItems"][products]["productName"]
                    quantity = request_data["orderItems"][products]["quantity"]
                    
                    try:
                        productObject = Product.objects.filter(name=product_name)
                        productData = ProductSerializer(productObject).data
                    except Exception as e:
                            error_message = str(e)
                            return JsonResponse({'error': error_message}, status=500)
 
                    if productData["quantity"] >= quantity:
                          OrderItemData = {"orderID" : order }
                    
                   
                    



            return JsonResponse({"data" : "data"}, status = 200)
        
        return JsonResponse({"data": "data"}, status = 200)
            


