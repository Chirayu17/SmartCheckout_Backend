from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import UserTokenAuthentication, UserPermission
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from inventory.models import Category, Product
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import  authentication_classes,permission_classes
from inventory.productSerializers import ProductSerializer, CategorySerializer
from users.userSerializers import UserSerializer
from orders.orderSerializer import OrderItemSerializer, OrderSerializer
from django.core import serializers as serial
import datetime
import base64
import binascii
from drf_yasg import openapi
from orders.models import OrderItem, Orders
from users.models import User
from orders.dataModel import ImageDetection
import io
from PIL import Image


class OrderView(APIView):
    @authentication_classes(UserTokenAuthentication)
    @permission_classes(UserPermission)


    def get(self, request, orderID = None):
        data = {}
        if orderID is None:
            orders = Orders.objects.filter(user =  request.user)
            if not orders:
                    error_message = "No order found."
                    return JsonResponse({'error': error_message}, status=404)
                
            order_serializer = OrderSerializer(orders, many = True)
            data = order_serializer.data
            return JsonResponse(data, content_type='application/json', status=200, safe=False)
        else:
            orders = Orders.objects.filter(orderID = orderID,user =  request.user)
            if not orders:
                    error_message = "No order found."
                    return JsonResponse({'error': error_message}, status=404)
                

            order_serializer = OrderSerializer(orders, many = True)

            data = order_serializer.data
            orderItems = OrderItem.objects.filter(orderID = data[0]["orderID"])

            orderIten_serializer = OrderItemSerializer(orderItems, many = True)
            orderItemObject = {"orderItems" :orderIten_serializer.data }
            data.append(orderItemObject)
            return JsonResponse(data, content_type='application/json', status=200, safe=False)



    def post(self, request, orderID = None):
        if orderID is None:
            data = {}
            order_items = {}
            total_price = 0

            try:
                userObject = User.objects.get(phoneNumber = request.user)
                user_serializer = UserSerializer(instance = userObject)
                userdata = user_serializer.data
            except Exception as e:
                        error_message = str(e)
                        return JsonResponse({'userError': error_message}, status=500)
            
            orderObject = {"user" : userObject.pk, "completed" :  False, "created_at" : datetime.datetime.now(), "total" : 0 }
            orderserialized  = OrderSerializer(data = orderObject)
            orderData = {}

            #orderCreation -->
            if orderserialized.is_valid():
                order_instance=orderserialized.save()
                orderData = serial.serialize('json', [order_instance,])
                print("type of orderData ->", type(orderData))
                data["order"] = json.loads(orderData)
            else:
                return JsonResponse({'error': orderserialized.errors})
            
            #orderItemCreation -->

            request_data = json.loads(request.body)
            try:
                image_data = base64.b64decode(request_data["image"])
            except binascii.Error:
                return HttpResponseBadRequest("Invalid base64 image")
            
            if not image_data:
                    return HttpResponseBadRequest("Empty decoded image data")
            
            image_stream = io.BytesIO(image_data)

            image = Image.open(image_stream)        
            # print("type of img", type(image))
            converted_image = image.convert("RGB")
            
            detectedOrder = ImageDetection(converted_image)
            if detectedOrder:
                  for categories in detectedOrder:  
                        for key in detectedOrder[categories]:
                            try:
                                product = Product.objects.filter(name__icontains=key).first()
                                print("product->", product)
                                if product:
                                    product_serializer = ProductSerializer(instance = product)
                                    productdata = product_serializer.data
                                    if productdata["quantity"] >= detectedOrder[categories][key]:
                        
                                        totalAmount = float(productdata["price"])* float(detectedOrder[categories][key])
                                        total_price += totalAmount
                                        orderitem = {"orderID" : order_instance.pk, "productID" : product.pk, "productName" : key, "user" : userObject.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : detectedOrder[categories][key], "total" : totalAmount, "unAvailable" : False,"outOfStock" : False, "completed" : True }
                                        orderItemSerialized  = OrderItemSerializer(data = orderitem)
                                        if orderItemSerialized.is_valid():
                                            orderItem_instance=orderItemSerialized.save()
                                            orderItemData = serial.serialize('json', [orderItem_instance,])
                                            order_items["available"] = json.loads(orderItemData)
                        
                                        else:
                                            return JsonResponse({'orderDataError': orderItemSerialized.errors})

                                    else:
                                        totalAmount = float(productdata["price"])* float(detectedOrder[categories][key])
                                        orderitem = {"orderID" : order_instance.pk, "productID" : product.pk,"productName" : key, "user" : userObject.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : detectedOrder[categories][key], "total" : totalAmount, "unAvailable" : False,"outOfStock" : True, "completed" : False }
                                        orderItemSerialized  = OrderItemSerializer(data = orderitem)
                                        if orderItemSerialized.is_valid():
                                            orderItem_instance=orderItemSerialized.save()
                                            orderItemData = serial.serialize('json', [orderItem_instance,])
                                            order_items["outOfStock"] = json.loads(orderItemData)
    
                                        else:
                                            return JsonResponse({'orderDataError': orderItemSerialized.errors})
                                        print( "There are only " + str(data["quantity"]) +  " " + str(data["name"]) + " " + " present in database") 
                                else:
                                   
                                    orderitem = {"orderID" : order_instance.pk, "productName" : key, "user" : userObject.pk, "created_at" : datetime.datetime.now(), "price" : 0, "quantity" : detectedOrder[categories][key], "total" : 0, "unAvailable" : True,"outOfStock" : True, "completed" : False }
                                    orderItemSerialized  = OrderItemSerializer(data = orderitem)
                                    if orderItemSerialized.is_valid():
                               
                                        orderItem_instance=orderItemSerialized.save()
                                        orderItemData = serial.serialize('json', [orderItem_instance,])
                                        order_items["unavailable"] = json.loads(orderItemData)
                                    else:
                                    
                                        return JsonResponse({'orderDataError': orderItemSerialized.errors})
                                  
                            except Exception as e:
                                error_message = str(e)
                                print({'product' : error_message})
                                # return JsonResponse({'error': error_message}, status=500)
            print("orderItems->", order_items)
            data["orderItems"] = order_items
            return JsonResponse({"data": data}, status = 200)
        
        else:
            request_data = json.loads(request.body)
            try:
                orderObject = Orders.objects.get(orderID = orderID)
                if orderObject:
                     if "image" in request_data:
                        try:
                            image_data = base64.b64decode(request_data["image"])
                        except binascii.Error:
                            return HttpResponseBadRequest("Invalid base64 image")
            
                        if not image_data:
                                return HttpResponseBadRequest("Empty decoded image data")
            
                        image_stream = io.BytesIO(image_data)

                        image = Image.open(image_stream)        
                        converted_image = image.convert("RGB")

                        detectedOrder = ImageDetection(converted_image)
                        if detectedOrder:

                            return JsonResponse({"image" :  request_data["image"]}, status = 200)
                order_serializer = OrderSerializer(instance = orderObject)
                orderdata = order_serializer.data
            except Exception as e:
                        error_message = str(e)
                        return JsonResponse({'orderError': error_message}, status=500)
            
            return JsonResponse({"data": "data"}, status = 200)
    # return JsonResponse({"data": data}, status = 200)
    
            

    def put(self, request, orderID = None):
         
         return JsonResponse({"data" : "data"}, status = 200)
