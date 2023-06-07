import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

import keys





class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request): 
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            raise AuthenticationFailed('User not logged in')


        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return None

        try:
            data = jwt.decode(token, keys.JWT_SECRET_admin, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError as e:
            print(e)
            raise AuthenticationFailed('Invalid token')
        return (data['phoneNumber'], None)
    

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return False

        try:
            jwt.decode(token, keys.JWT_SECRET_admin, algorithms=['HS256'])
            return True
        except jwt.exceptions.InvalidTokenError:
            return False