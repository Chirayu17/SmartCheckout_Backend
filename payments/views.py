from django.shortcuts import render
from rest_framework.views import APIView
from users.authentication import TokenAuthentication, Permission
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from inventory.models import Category, Product
from orders.models import OrderItem, Orders
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import  authentication_classes,permission_classes
from users.userSerializers import UserSerializer
from orders.orderSerializer import OrderSerializer, OrderItemSerializer
from payments.paymentSerializers import PaymentSerializer
from django.core import serializers as serial
import datetime
import base64
import binascii
from drf_yasg import openapi
from orders.models import  Orders
from users.models import User

import io
from PIL import Image

import random


# Create your views here.

class PaymentView(APIView):
    @authentication_classes(TokenAuthentication)
    @permission_classes(Permission)


    def post(self, request):
        request_data = json.loads(request.body)
        data = {}
        paymentObject = {"orderID" : request_data["orderID"], "created_at" :  datetime.datetime.now(), "modified_at" : datetime.datetime.now(), "user" : request.user, "amount" : request_data["amount"], "completed" : True}
        paymentserialized  = PaymentSerializer(data = paymentObject)

        if paymentserialized.is_valid():
            payment_instance=paymentserialized.save()
            paymentData = serial.serialize('json', [payment_instance,])
            paymentJsonData = json.loads(paymentData)[0]
            paymentJsonData["fields"]["paymentID"] = paymentJsonData["pk"]
            data["payment"] = paymentJsonData["fields"]

            order = Orders.objects.filter(orderID = request_data["orderID"])
            order_data = {}
            order_data["completed"] = True
            serializer = OrderSerializer(instance=order, data=order_data, partial=True)
            if serializer.is_valid():
                order_instance = serializer.save()
                data = serial.serialize('json', [order_instance,])
                return JsonResponse({"data": data})
            else:
                print("Couldn't update Order")
                # return JsonResponse({'error': serializer.errors}, status=400)


            orderItems = OrderItem.objects.filter(orderID = request_data["orderID"])

            

            orderItem_serializer = OrderItemSerializer(orderItems, many = True)
            orderItemObject = orderItem_serializer.data

            for orderItem in orderItemObject:
                productInstance = Product.objects.get(name = orderItem["productID"])
                productInstance.quantity = productInstance.quantity - orderItem["quantity"]
                productInstance.save()
        else:
            return JsonResponse({'error': paymentserialized.errors})
        
        return JsonResponse({"data" : orderItemObject}, status = 200)
