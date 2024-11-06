from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema

# Vue d'inscription
class RegisterView(APIView):
    permission_classes = [AllowAny]
    #pour la documentation 
    @swagger_auto_schema(request_body=RegisterSerializer)
    #methode de register
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
             # convert user data to json 
            user_data = UserSerializer(user).data
            #token
            tokens=serializer.get_tokens(user)
            return JsonResponse({'message': 'User registered successfully',
                             'user':user_data,
                             'acess_token':tokens["access"],
                             'refresh':tokens["refresh"]
                             }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue de login
class LoginView(APIView):
    permission_classes = [AllowAny]
     #pour la documentation 
    @swagger_auto_schema(request_body=RegisterSerializer)
    #methode de login

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # convert user data to json 
            user_data = UserSerializer(user).data
            # recuperer les tokens
            tokens = serializer.get_tokens(user)
            
            return Response({'message': 'User login successfully',
                             'user':user_data,
                             'acess_token':tokens["access"],
                             'refresh':tokens["refresh"]
                             }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
