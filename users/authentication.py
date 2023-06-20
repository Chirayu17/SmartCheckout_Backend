import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
 
JWT_SECRET = "SmartCheckout"





class TokenAuthentication(BaseAuthentication):
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
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError as e:
            print(e)
            raise AuthenticationFailed('Invalid token')
        return (data['phoneNumber'], None)
    
    
        

class Permission(BasePermission):
    def has_permission(self, request, view):
        print("in permission")
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return False

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return False

        try:
            decoded_data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            role = decoded_data['role']  # Assuming the role is included in the token data
        except jwt.exceptions.InvalidTokenError:
            return False

        if view.__class__.__name__ == 'ProductView':
            # Only admins have permission for the product API
            if role == 'admin':
                return True
            else:
                return False

        if view.__class__.__name__ == 'OrderView':
            # Only users have permission for the orders API
            if role == 'user':
                return True
            else:
                return False

        return False
