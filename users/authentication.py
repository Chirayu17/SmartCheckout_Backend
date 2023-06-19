import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
 
JWT_SECRET_admin = "SmartCheckoutadmin"
JWT_SECRET_user = 'SmartCheckoutretail'





class UserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request): 
        print("in user token authentication")
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            raise AuthenticationFailed('User not logged in')


        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return None

        try:
            data = jwt.decode(token, JWT_SECRET_user, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError as e:
            print(e)
            raise AuthenticationFailed('Invalid token')
        return (data['phoneNumber'], None)
    
class AdminTokenAuthentication(BaseAuthentication):
    def authenticate(self, request): 
        print("in admin token authentication")
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            raise AuthenticationFailed('User not logged in')


        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return None

        try:
            data = jwt.decode(token, JWT_SECRET_admin, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError as e:
            print(e)
            raise AuthenticationFailed('Invalid token')
        return (data['phoneNumber'], None)
    

class AdminPermission(BasePermission):
    print("in admin permission")
    def has_permission(self, request, view):
        
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return False

        try:
            jwt.decode(token, JWT_SECRET_admin, algorithms=['HS256'])
            return True
        except jwt.exceptions.InvalidTokenError:
            return False
        

class UserPermission(BasePermission):
    print("in user permission")
    def has_permission(self, request, view):
        
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return False

        try:
            jwt.decode(token, JWT_SECRET_user, algorithms=['HS256'])
            return True
        except jwt.exceptions.InvalidTokenError:
            return False