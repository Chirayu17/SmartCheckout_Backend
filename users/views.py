from django.shortcuts import render
import jwt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from rest_framework.decorators import  authentication_classes,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from users.models import admin_user, Cashier, User
from django.db.models import Q
from users.userSerializers import UserSerializer, admin_userSerializer, CashierSerializer
from datetime import datetime
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema




JWT_SECRET = 'SmartCheckout'

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Enter your username'),
            'email':openapi.Schema(type=openapi.TYPE_STRING,description='Enter you email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Enter your password')
        },
    ),
    responses={
        201: 'Created',
        400: 'Bad Request'
    },
    operation_summary='SigUup for new User',
    operation_description='API endpoint to signup a new user'
)

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signup(request):
    
    if request.path == '/signup/admin/': 
        try:
            data = request.data if request.data is not None else {}
            required_fields = set(['name', 'email', 'password', 'phoneNumber','username'])
            if not required_fields.issubset(data.keys()):
                return JsonResponse(status=400, data={'error': 'Missing required fields'})
            existing_user = admin_user.objects.filter(Q(phoneNumber=data['phoneNumber']) | Q(email=data['email']))
            if existing_user:
                return JsonResponse(status=409, data={'error': 'User with the same phone number or email already exists'})
            password_hash = pbkdf2_sha256.hash(data['password'])
            admin_userData = {
                'name': data['name'],
                'phoneNumber' : data['phoneNumber'],
                'created_at' : datetime.now,
                'isActive' : True,
                'email': data['email'],
                'password': str(password_hash),
                'username' : data['username']
            }
            serializer = admin_userSerializer(data = admin_userData)
            if serializer.is_valid():
                print("here")
                instance=serializer.save()
            else:
                return JsonResponse({'error': serializer.error})

            token = jwt.encode({'username': data['username'], 'exp': datetime.utcnow() + timedelta(hours=1), 'role' : 'admin'} , JWT_SECRET)
            return JsonResponse(status=status.HTTP_201_CREATED, data={'token': token, 'statusText': 'User Created'})

        except Exception as e:
            return JsonResponse(status=500, data={'error': str(e)})
    elif request.path == '/signup/cashier/':
        try:
            data = request.data if request.data is not None else {}
            required_fields = set(['name', 'email', 'password', 'phoneNumber',])
            if not required_fields.issubset(data.keys()):
                return JsonResponse(status=400, data={'error': 'Missing required fields'})
            existing_user = Cashier.objects.filter(Q(phoneNumber=data['phoneNumber']) | Q(email=data['email']))
            if existing_user:
                return JsonResponse(status=409, data={'error': 'User with the same phone number or email already exists'})
            password_hash = pbkdf2_sha256.hash(data['password'])
            cashierData = {
                'name': data['name'],
                'phoneNumber' : data['phoneNumber'],
                'created_at' : datetime.now,
                'isActive' : True,
                'email': data['email'],
                'password': str(password_hash)
            }
            serializer = CashierSerializer(data = cashierData)
            if serializer.is_valid():
                print("here")
                instance=serializer.save()
            else:
                return JsonResponse({'error': serializer.error})

            token = jwt.encode({'phoneNumber': data['phoneNumber'], 'exp': datetime.utcnow() + timedelta(hours=1), 'role' : 'cashier'} , JWT_SECRET)
            return JsonResponse(status=status.HTTP_201_CREATED, data={'token': token, 'statusText': 'User Created'})

        except Exception as e:
            return JsonResponse(status=500, data={'error': str(e)})
        
    elif request.path == '/signup/user/':
        try:
            data = request.data if request.data is not None else {}
            print("data->", data)
            required_fields = set(['name','phoneNumber', 'created_by'])
            if not required_fields.issubset(data.keys()):
                return JsonResponse(status=400, data={'error': 'Missing required fields'})
            existing_user = User.objects.filter(phoneNumber=data['phoneNumber'])
            if existing_user:
                return JsonResponse(status=409, data={'error': 'User with the same phone number already exists'})
    
            userData = {
                'name': data['name'],
                'phoneNumber' : data['phoneNumber'],
                'created_at' : datetime.now,
                'isActive' : True,
                'created_by': data["created_by"]
            }
            print("userData->", userData)
            serializer = UserSerializer(data = userData)
            if serializer.is_valid():
                instance=serializer.save()
            else:
                print("here")
                return JsonResponse({'error': serializer.errors})

            token = jwt.encode({'phoneNumber': data['phoneNumber'], 'exp': datetime.utcnow() + timedelta(hours=5), 'role' : 'user'} , JWT_SECRET)
            return JsonResponse(status=status.HTTP_201_CREATED, data={'token': token, 'statusText': 'User Created'})

        except Exception as e:
            return JsonResponse(status=500, data={'error': str(e)})

    return JsonResponse(status= 400, data = {'error' : "Couldn't signup"})


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Enter your username'),
            'email':openapi.Schema(type=openapi.TYPE_STRING,description='Enter you email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Enter your password')
        },
    ),
    responses={
        201: 'Created',
        400: 'Bad Request'
    },
    operation_summary='SigUup for new User',
    operation_description='API endpoint to signup a new user'
)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])

def login(request):

    if request.path == '/auth/user/login': 
        print("here in loginUser")
        try:
            data = request.data if request.data is not None else {}
            print("data ->", data)
            print("type ->", type(data['phoneNumber']))
            required_fields = set(['phoneNumber'])
            if not required_fields.issubset(data.keys()):
                return JsonResponse(status=400, data={'error': 'Missing required fields'})
            try:
                existing_user = User.objects.get(phoneNumber = data['phoneNumber'])
                if existing_user :
                    token = jwt.encode({'phoneNumber': data['phoneNumber'], 'exp': datetime.utcnow() + timedelta(hours=1), 'role' : 'user'} , JWT_SECRET)
                    return JsonResponse(status=200, data= {'username':existing_user.name, 'token' : token})
            except:
                    print("user not found")
                    return JsonResponse(status=404, data= {'error': "user not found in db"})
        except Exception as e:
            return JsonResponse(status=500, data={'error': str(e)}) 

    elif request.path == '/auth/admin/login': 
        try:
            data = request.data if request.data is not None else {}
            required_fields = set(['password', 'username'])
            if not required_fields.issubset(data.keys()):
                return JsonResponse(status=400, data={'error': 'Missing required fields'})
            user = admin_user.objects.get(username= data['username'])
            print((user))
            if user and pbkdf2_sha256.verify(data['password'], user.password):
                token = jwt.encode({'username': data['username'], 'exp': datetime.utcnow() + timedelta(hours=1), 'role' : 'admin'} , JWT_SECRET)
                return JsonResponse(status=200, data={'token': token})
            else:
                return JsonResponse(status=401, data={'error': 'Invalid phoneNumber or password'})
        except Exception as e:
            return JsonResponse(status=500, data={'error': str(e)})
        
    elif request.path == '/auth/cashier/login': 
        try:
            data = request.data if request.data is not None else {}
            required_fields = set(['password', 'phoneNumber'])
            if not required_fields.issubset(data.keys()):
                return JsonResponse(status=400, data={'error': 'Missing required fields'})
            user = Cashier.objects.get(phoneNumber= data['phoneNumber'])
            print((user))
            if user and pbkdf2_sha256.verify(data['password'], user.password):
                token = jwt.encode({'phoneNumber': data['phoneNumber'], 'exp': datetime.utcnow() + timedelta(hours=1), 'role' : 'cashier'} , JWT_SECRET)
                return JsonResponse(status=200, data={'token': token})
            else:
                return JsonResponse(status=401, data={'error': 'Invalid phoneNumber or password'})
        except Exception as e:
            return JsonResponse(status=500, data={'error': str(e)})
        
    return JsonResponse(status =404, data = {'error' : "user not found"})