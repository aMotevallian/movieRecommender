from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from ..serializers import RegisterSerializer
from django.http import JsonResponse

# Register API
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'detail': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)

# class LoginAPI(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             response = JsonResponse({'message': 'Login successful'})
#             response.set_cookie(
#                 key='token',
#                 value=token.key,
#                 httponly=True,
#                 secure=True,     # Use True in production
#                 samesite='None'   # Adjust as per needs
#             )
#             return response
#         else:
#             return Response({'error': 'Invalid Credentials'}, status=400)

# class TokenValidateAPI(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         user = request.user
#         return Response({'username': user.username, 'email': user.email})
class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = JsonResponse({'detail': 'Logged out successfully'})
        response.delete_cookie('token')  # Clear the token cookie
        return response
