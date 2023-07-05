from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import TokenAuthentication, Permission
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
# from orders.dataModel import ImageDetection
import io
from PIL import Image
from orders.createOrderItem import createOrderItem, updateOrder
import random
# from ImageDetection.main import ProcessImage
from DataScience.processImage import ProcessImage

class OrderView(APIView):
    @authentication_classes(TokenAuthentication)
    @permission_classes(Permission)


    def get(self, request, orderID = None):
        data = {}
        if orderID is None:
            latest_order = Orders.objects.filter(user=request.user, completed=False).order_by('-created_at').first()
            if latest_order:
                order_serializer = OrderSerializer(latest_order, many = True)
                data = order_serializer.data
                return JsonResponse(data, content_type='application/json', status=200, safe=False)
            else:
                return JsonResponse({"message" : "No order found"})
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
            print("user->" , request.user)
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
                data["order"] = json.loads(orderData)[0]
            else:
                return JsonResponse({'error': orderserialized.errors})
            
            #orderItemCreation -->

            # request_data = json.loads(request.body)
            # try:
            #     image_data = base64.b64decode(request_data["image"])
            # except binascii.Error:
            #     return JsonResponse({"error" : "Invalid base64 image"}, status = 400)
            
            # if not image_data:
            #         return JsonResponse({"error" :"Empty decoded image data"}, status = 400)
            
            # image_stream = io.BytesIO(image_data)

            # image = Image.open(image_stream)        
          
            # converted_image = image.convert("RGB")
            # print("type of->", type(converted_image))


            
            # detectedOrder = ImageDetection(converted_image)
            # print("detected Order ->", detectedOrder)
            # if not detectedOrder:
            #     data["orderItems"] = "Unable to detect items in image. Try it again"
            #     return JsonResponse({"data": data}, status = 400)
            # else:
            #     data["orderItems"] = createOrderItem(detectedOrder, data, order_instance, userObject, total_price)
            
          
        return JsonResponse({"data" : data}, status = 200)
    

    def put(self, request, orderID = None, orderItemID = None): 
        
        if orderID is None:
            error_message = "Provide order ID"
            return JsonResponse({'orderError': error_message}, status=500)

        else:
            print("In else")
            request_data = json.loads(request.body)
            if orderItemID is None:
                data = {}
                
                try:
                    orderObject = Orders.objects.get(orderID = orderID)
                    if orderObject: 
                        
                        if "image" in request_data:
                            print("here")
                            try:
                                image_data = base64.b64decode(request_data["image"])
                                existingData = {}
                                existingData["existingOrderItems"] = request_data["existingOrderItems"]
                            except binascii.Error:
                                return JsonResponse({"error" : "Invalid base64 image"}, status = 400)
                
                            if not image_data:
                                    return JsonResponse({"error" :"Empty decoded image data"}, status = 400)
                
                            image_stream = io.BytesIO(image_data)

                            image = Image.open(image_stream)        
                            converted_image = image.convert("RGB")

                            # detectedOrder = ImageDetection(converted_image)
                            
                            # if detectedOrder:
                            #     data = updateOrder(detectedOrder, existingData, orderObject, orderObject.user, 0)
                            #     return JsonResponse({"data" : data}, status = 200)
                            # else: 
                            #     data = "Unable to detect items in image. Try it again"
                            #     return JsonResponse({"data" : data}, status = 404)

                            process_image = ProcessImage(request_data["image"])
                            processed_image = process_image.run()
                            print(processed_image)
                            if processed_image is not None:
                                # Print the results or perform further processing
                                # for elements in processed_image:
                                #     print("elements->", elements)
                                data = updateOrder(processed_image, existingData, orderObject, orderObject.user, 0)
                                # print("data->", data)
                                return JsonResponse(data, status = 200,safe= False)
                            else:
                                data = "Unable to detect items in image. Try it again"
                                return JsonResponse({"data" : data}, status = 404, safe= False)

                            

                       
                            
                        elif "newOrderItem" in request_data:
                            orderItem = request_data["newOrderItem"]
                            productObject = Product.objects.filter(name__icontains=orderItem["name"]).first()
                            print("product->", productObject)
                            if productObject:
                                    product_serializer = ProductSerializer(instance = productObject)
                                    productdata = product_serializer.data
                            if productdata["quantity"] >= orderItem["quantity"]:
                                totalAmount = float(productdata["price"])* float(orderItem["quantity"])
                                print("order user->", orderObject.user)
                                orderItemData = {"orderID" : orderObject.pk, "productID" : productObject.pk,"productName" :  productObject.name, "user" : orderObject.user.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : orderItem["quantity"], "total" : totalAmount, "completed" : False }

                                orderItemSerialized  = OrderItemSerializer(data = orderItemData)
                                if orderItemSerialized.is_valid():
                                    orderItem_instance=orderItemSerialized.save()

                                    orderItemJson = serial.serialize('json', [orderItem_instance,])
                                    print("orderrrrrrrrrr",orderItemJson)
                                    newOrderItemJson = json.loads(orderItemJson)
                                    
                                    orderItemJsonData = newOrderItemJson[0]["fields"]

                                   
                                    orderItemJsonData["imgSrc"] = productdata["image"]
                                    orderItemJsonData["orderItemID"] = newOrderItemJson[0]["pk"]
                                    data["available"] = orderItemJsonData
                                    return JsonResponse({"data": data}, status = 200)

                                else:
                                    return JsonResponse({'orderItemDataError': orderItemSerialized.errors}, status = 200)
                            else:
                                message =  "There are only " + str(productdata["quantity"]) +  " " + str(productdata["name"]) + " " + " present in stock"
                                orderItem = {}
                                orderItem[productdata["name"]] = message
                                data["outOfStock"] = orderItem
                   
                        
                            
                    else:
                        error_message = "No order found with orderID " + orderID  
                        return JsonResponse({"error" : error_message}, status = 400)
                except Exception as e:
                            error_message = str(e)
                            return JsonResponse({'orderError': error_message}, status=500)
                            
            else :
                productObject = Product.objects.get(name = request_data["productID"])
                if productObject.quantity>= request_data["quantity"]:
                    print("here in if")
                    orderItem =  OrderItem.objects.get(id = orderItemID)
                    orderItemData = {
                        "total" : float(productObject.price)* float( request_data["quantity"]),
                        "quantity" : request_data["quantity"],
                    }
                    print(orderItemData)
                    serializer = OrderItemSerializer(instance= orderItem, data= orderItemData, partial=True)
                    if serializer.is_valid():
                        product_instance = serializer.save()
                        data = serial.serialize('json', [product_instance,])
                        jsonData = json.loads(data)
                        return JsonResponse({"data": jsonData[0]["fields"]})
                    else:
                        return JsonResponse({'error': serializer.errors}, status=400)
                else:
                        print("here in else")
                        error_message = "There are only " + str(productObject.quantity) + " " + productObject.name + " in inventory"
                        return JsonResponse({'error' : error_message}, status = 404)

            
            return JsonResponse({"data": "data"}, status = 200)





    def delete(self, request, orderID = None, orderItemID = None): 
        if orderID is None:
            error_message = "Provide order ID"
            return JsonResponse({'orderError': error_message}, status=500)
        else:
            if orderItemID is None:
                print("here")
                result = OrderItem.objects.filter(orderID=orderID).delete()
                if result[0] > 0:
                        return JsonResponse({'message': "order item deleted successfully"}, status= 200)
                else:
                        return JsonResponse({'error': "Unable to find item"}, status= 404)
            else:
                try:
                    result = OrderItem.objects.filter(id=orderItemID).delete()
                    if result[0] > 0:
                            return JsonResponse({'message': "order item deleted successfully"}, status= 200)
                    else:
                            return JsonResponse({'error': "Unable to find item"}, status= 404)
                except Exception as e:
                        error_message = str(e)
                        return JsonResponse({'orderItemError': error_message}, status=500)
                

       
    