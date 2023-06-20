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
        for key in detectedOrder[categories]:
            try:
                product = Product.objects.filter(name__icontains=key).first()
                print("product->", product)
                if product:
                    product_serializer = ProductSerializer(instance = product)
                    productdata = product_serializer.data
                    if productdata["quantity"] >= detectedOrder[categories][key]:
        
                        totalAmount = float(productdata["price"])* float(detectedOrder[categories][key])
                        data["totalAmount"] =  data["totalAmount"] + totalAmount
                       
                        orderitem = {"orderID" : order_instance.pk, "productID" : product.pk, "productName" : key, "user" : userObject.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : detectedOrder[categories][key], "total" : totalAmount, "unAvailable" : False,"outOfStock" : False, "completed" : True, "addedManually" : False, "updatedManually" : False, "probability" : round(random.uniform(0.4, 0.9), 2)}
                        orderItemSerialized  = OrderItemSerializer(data = orderitem)
                        if orderItemSerialized.is_valid():
                            orderItem_instance=orderItemSerialized.save()
                            orderItemData = serial.serialize('json', [orderItem_instance,])
                            order_items["available"].append(json.loads(orderItemData)[0])
                        else:
                            return JsonResponse({'orderDataError': orderItemSerialized.errors})

                    else:
                        message =  "There are only " + str(productdata["quantity"]) +  " " + str(productdata["name"]) + " " + " present in stock"
                        orderItem = {}
                        orderItem[key] = message
                        order_items["outOfStock"].append(orderItem)
                       
                else:
                    message =  str(key) + " " + " is not in stock. Kindly try again"
                    orderItem = {}
                    orderItem[key] = message
                    order_items["unavailable"].append(orderItem)
                    
            except Exception as e:
                error_message = str(e)
                print({'product' : error_message})
                                # return JsonResponse({'error': error_message}, status=500)
    return order_items


def updateOrder(detectedOrder,data, order_instance,userObject, total_price, existingOrderItems):
        order_items = {}
        order_items["available"] = []
        order_items["outOfStock"] = []
        order_items["unavailable"] = []
        
        print("order ->", order_instance)
        print("user->", userObject)
        for categories in detectedOrder:  
            for key in detectedOrder[categories]:
                try:
                    product = Product.objects.filter(name__icontains=key).first()
                    print("product->", product)

                    if product:
                        
                        product_serializer = ProductSerializer(instance = product)
                        productdata = product_serializer.data
                        for existingOrderObject in existingOrderItems:
                            print("existingOrderObject->",existingOrderObject.productID)
                            if productdata["name"] == existingOrderObject.productID:
                                totalQuantity = existingOrderObject.quantity + detectedOrder[categories][key]
                                if productdata["quantity"] >= totalQuantity:
                                    print("quantity ->", existingOrderObject.quantity)
                                    existingOrderObject.quantity = totalQuantity
                                    existingOrderObject.save()
                                else:
                                    error_message = "There are only " + productdata["quantity"] + " in stock."

                                    return JsonResponse({"outOfStock" : error_message}, status = 404)
                            else:
                                if productdata["quantity"] >= detectedOrder[categories][key]:
                                    totalAmount = float(productdata["price"])* float(detectedOrder[categories][key])
                                    total_price += totalAmount
                                    orderitemData = {"orderID" : order_instance.pk, "productID" : product.pk, "productName" : key, "user" : userObject.pk, "created_at" : datetime.datetime.now(), "price" : productdata["price"], "quantity" : detectedOrder[categories][key], "total" : totalAmount, "unAvailable" : False,"outOfStock" : False, "completed" : True, "addedManually" : False, "updatedManually" : False, "probability" : round(random.uniform(0.4, 0.9), 2)}
                                    orderItemSerialized  = OrderItemSerializer(data = orderitemData)
                                    if orderItemSerialized.is_valid():
                                        orderItem_instance=orderItemSerialized.save()
                                        orderitemData = serial.serialize('json', [orderItem_instance,])
                                        order_items["available"] = json.loads(orderitemData)
                    
                                    else:
                                        return JsonResponse({'orderItemDataError': orderItemSerialized.errors})

                                else:
                                      message =  "There are only " + str(productdata["quantity"]) +  " " + str(productdata["name"]) + " " + " present in stock"
                                      orderItem = {}
                                      orderItem[key] = message
                                      order_items["outOfStock"].append(orderItem)
                                    
                    else: 
                        message =  str(key) + " " + " is not in stock. Kindly try again"
                        orderItem = {}
                        orderItem[key] = message
                        order_items["unavailable"].append(orderItem)
                        
                except Exception as e:
                    error_message = str(e)
                    print({'product' : error_message})
                                    # return JsonResponse({'error': error_message}, status=500)
        return order_items
