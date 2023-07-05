from inventory.models import Product
from inventory.productSerializers import ProductSerializer
from orders.orderSerializer import OrderItemSerializer
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from orders.models import OrderItem
import json
from django.core import serializers as serial
import datetime
import random

def createOrderItem(detectedOrder, data, order_instance, userObject, total_price):
    order_items = {}
    order_items["available"] = []
    order_items["outOfStock"] = []
    order_items["unavailable"] = []
    data["totalAmount"] = 0

    for categories in detectedOrder:  
            try:
                product = Product.objects.filter(name__icontains=categories).first()
                print("product->", product)
                if product:
                    product_serializer = ProductSerializer(instance = product)
                    productdata = product_serializer.data
                    if productdata["quantity"] >= detectedOrder[categories][categories]:
        
                        totalAmount = float(productdata["price"])* float(detectedOrder[categories][categories])
                        data["totalAmount"] =  data["totalAmount"] + totalAmount
                       
                        orderitem = {"orderID" : order_instance.pk, "productID" : product.pk, "productName" : categories, "user" : userObject.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : detectedOrder[categories], "total" : totalAmount, "unAvailable" : False, "addedManually" : False, "updatedManually" : False, "probability" : round(random.uniform(0.4, 0.9), 2)}
                        orderItemSerialized  = OrderItemSerializer(data = orderitem)
                        if orderItemSerialized.is_valid():
                            orderItem_instance=orderItemSerialized.save()
                            orderItemData = serial.serialize('json', [orderItem_instance,])
                            orderItemJsonData = json.loads((orderItemData))[0]
                            print("orderItemJsonData->", orderItemJsonData)
                            orderItemJsonData["fields"]["orderItemID"] = orderItemJsonData["pk"]
                            orderItemJsonData["fields"]["imgSrc"] = productdata["image"]
                            order_items["available"].append(orderItemJsonData)
                        else:
                            return JsonResponse({'orderDataError': orderItemSerialized.errors})

                    else:
                        message =  "There are only " + str(productdata["quantity"]) +  " " + str(productdata["name"]) + " " + " present in stock"
                        orderItem = {}
                        orderItem[categories] = message
                        order_items["outOfStock"].append(orderItem)
                       
                else:
                    message =  str(categories) + " " + " is not in stock. Kindly try again"
                    orderItem = {}
                    orderItem[categories] = message
                    order_items["unavailable"].append(orderItem)
                    
            except Exception as e:
                error_message = str(e)
                print({'product' : error_message})
                                # return JsonResponse({'error': error_message}, status=500)
    return order_items


def updateOrder(detectedOrder,existingData, order_instance,userObject, total_price):
        order_items = {}
        order_items["available"] = existingData["existingOrderItems"]
        order_items["outOfStock"] = []
        order_items["unavailable"] = []
        itemList = []
        for existingOrderItems in existingData["existingOrderItems"]:
            itemList.append(existingOrderItems["productID"])
        
        print(itemList)
        
        
        for categories in detectedOrder:  
            print("here")
            try:
                product = Product.objects.filter(name__icontains=categories).first()
                print("product->", product)

                if product:
                    
                    product_serializer = ProductSerializer(instance = product)
                    productdata = product_serializer.data
                    if productdata["name"] in itemList:
                        for existingOrderItems in order_items["available"]:
                            if productdata["name"] == existingOrderItems["productID"]:

                                totalQuantity = existingOrderItems["quantity"] + detectedOrder[categories]["counts"]
                                if productdata["quantity"] >= totalQuantity:
                                    orderItem =  OrderItem.objects.get(id = existingOrderItems["orderItemID"])
                                    orderItemData = {}
                                    orderItemData["quantity"] = totalQuantity
                                    orderItemData["total"] = float(productdata["price"])* float(totalQuantity)

                                    print(orderItemData)
                                    serializer = OrderItemSerializer(instance= orderItem, data= orderItemData, partial=True)
                                    if serializer.is_valid():
                                        print("here")
                                        orderItem_instance = serializer.save()
                                        existingOrderItems["quantity"] = totalQuantity
                                        existingOrderItems["total"]= float(productdata["price"])* float(totalQuantity)
                                        # data = serial.serialize('json', [product_instance,])

                                        # return JsonResponse({"data": [jsonData]})
                                    else:
                                        return serializer.errors


                                else:
                                    error_message = "There are only " + productdata["quantity"] + " in stock."

                                    return error_message
                    else:
                        if productdata["quantity"] >= detectedOrder[categories]["counts"]:
                            totalAmount = float(productdata["price"])* float(detectedOrder[categories]["counts"])
                            orderitemObject = {"orderID" : order_instance.pk, "productID" : product.pk, "productName" : categories, "user" : userObject.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : detectedOrder[categories]["counts"], "total" : totalAmount, "completed" : True, "addedManually" : False, "updatedManually" : False, "probability" : detectedOrder[categories]["probability"]}
                            orderItemSerialized  = OrderItemSerializer(data = orderitemObject)
                            if orderItemSerialized.is_valid():
                                print("here")
                                orderItem_instance=orderItemSerialized.save()
                                orderItemData = serial.serialize('json', [orderItem_instance,])
                                orderItemJsonData = json.loads((orderItemData))[0]
                                orderItemJsonData["fields"]["orderItemID"] = orderItemJsonData["pk"]
                                orderItemJsonData["fields"]["imgSrc"] = productdata["image"]
                                order_items["available"].append(orderItemJsonData["fields"])
                                print("orderITems->", order_items)
            
                            else:
                                return orderItemSerialized.errors

                        else:
                            message =  "There are only " + str(productdata["quantity"]) +  " " + str(productdata["name"]) + " " + " present in stock"
                            orderItem = {}
                            orderItem[categories] = message
                            order_items["outOfStock"].append(orderItem)
                                
                else: 
                    message =  str(categories) + " " + " is not in stock."
                    orderItem = {}
                    orderItem[categories] = message
                    order_items["unavailable"].append(orderItem)
                    
            except Exception as e:
                error_message = str(e)
                print({'product' : error_message})
                                # return JsonResponse({'error': error_message}, status=500)
        return order_items
