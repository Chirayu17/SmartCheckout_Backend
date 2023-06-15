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
from orders.createOrderItem import createOrderItem, updateOrder
import random



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

        try:
            userObject = User.objects.get(phoneNumber = request.user)
            user_serializer = UserSerializer(instance = userObject)
            userdata = user_serializer.data
        except Exception as e:
                    error_message = str(e)
                    return JsonResponse({'userError': error_message}, status=500)
        if orderID is None:
            data = {}
            order_items = {}
            total_price = 0

            
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
          
            converted_image = image.convert("RGB")
            
            detectedOrder = ImageDetection(converted_image)
            if detectedOrder:
                data["orderItems"] = createOrderItem(detectedOrder, data, order_instance, userObject, total_price)
            else:
                data["orderItems"] = "Unable to detect items in image. Try it again"
                return JsonResponse({"data": data}, status = 400)
            
          
        return JsonResponse({"data" : data}, status = 200)
    

    def put(self, request, orderID = None, orderItemID = None): 
        
        if orderID is None:
            error_message = "Provide order ID"
            return JsonResponse({'orderError': error_message}, status=500)

        else:
            #adding a new orderItemID in already created order -->
            if orderItemID is None:
                data = {}
                
                request_data = json.loads(request.body)
                try:
                    orderObject = Orders.objects.get(orderID = orderID)
                    if orderObject:
                       
                        existingOrderItems = OrderItem.objects.filter(orderID = orderID)
                        if existingOrderItems:
                            orderItem_serializer = OrderItemSerializer(existingOrderItems, many = True)
                            data["existingOrderItems"] = orderItem_serializer.data

                         #from image:   
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
                                data["orderItems"] = updateOrder(detectedOrder, data, orderObject, orderObject.user, 0, existingOrderItems)
                            else: 
                                data["orderItems"] = "Unable to detect items in image. Try it again"
                            
                            return JsonResponse({"data" : data}, status = 200)

                            
                        elif "newOrderItem" in request_data:
                            orderItem = request_data["newOrderItem"]
                            # productObject = Product.objects.filter(name__icontains=orderItem["name"]).first()
                            # print("product->", productObject)
                            # if productObject:
                            #         product_serializer = ProductSerializer(instance = productObject)
                            #         productdata = product_serializer.data
                            # if productdata["quantity"] >= orderItem["quantity"]:
                            #     totalAmount = float(productdata["price"])* float(orderItem["quantity"])
                            #     print("order user->", orderObject.user)
                            #     orderItemData = {"orderID" : orderObject.pk, "productID" : productObject.pk,"productName" :  productObject.name, "user" : orderObject.user.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : orderItem["quantity"], "total" : totalAmount, "unAvailable" : False,"outOfStock" : False, "completed" : False }

                            orderItemSerialized  = OrderItemSerializer(data = orderItem)
                            if orderItemSerialized.is_valid():
                                orderItem_instance=orderItemSerialized.save()
                                data["available"] = serial.serialize('json', [orderItem_instance,])

                            
                            else:
                                return JsonResponse({'orderItemDataError': orderItemSerialized.errors}, status = 200)
                            return JsonResponse({'data': data}, status = 200)
                            
                    else:
                        error_message = "No order found with orderID " + orderID  
                        return JsonResponse({"error" : error_message}, status = 400)
                except Exception as e:
                            error_message = str(e)
                            return JsonResponse({'orderError': error_message}, status=500)
                            

            else:
                orderItemData = json.loads(request.body)
                productObject = Product.objects.get(name = orderItemData["productID"])
                if productObject.quantity>= orderItemData["quantity"]:
                    orderItem =  OrderItem.objects.get(id = orderItemID)
                    orderItemData["total"] = float(productObject.price)* float( orderItemData["quantity"])
                    print(orderItemData)
                    serializer = OrderItemSerializer(instance= orderItem, data= orderItemData, partial=True)
                    if serializer.is_valid():
                        product_instance = serializer.save()
                        data = serial.serialize('json', [product_instance,])
                        return JsonResponse({"data": data})
                    else:
                        return JsonResponse({'error': serializer.errors}, status=400)
                else:
                     error_message = "There are only " + productObject.quantity + " " + productObject.name + " in inventory"
                     return JsonResponse({'error' : error_message}, status = 404)

                # return JsonResponse({"data" : "data"}, status = 200)    

            
            return JsonResponse({"data": "data"}, status = 200)

            

    def delete(self, request, orderID = None, orderItemID = None): 
         
         return JsonResponse({"data" : "data"}, status = 200)
    