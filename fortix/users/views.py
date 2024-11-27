import logging
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from users.models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema

# Configure the logger
logger = logging.getLogger(__name__)

# Vue d'inscription
class RegisterView(APIView):
    permission_classes = [AllowAny]

    # Pour la documentation
    @swagger_auto_schema(request_body=RegisterSerializer)
    # Méthode de register
    def post(self, request, *args, **kwargs):
        logger.info("Received data for registration: %s", request.data)  # Log input data
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                user_data = UserSerializer(user).data
                tokens = serializer.get_tokens(user)
                
                logger.info("User registered successfully: %s", user_data)  # Log successful registration
                return JsonResponse({
                    'message': 'User registered successfully',
                    'user': user_data,
                    'access_token': tokens["access"],
                    'refresh': tokens["refresh"]
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error("Error during user registration: %s", str(e))  # Log any exceptions
                return JsonResponse({
                    'error': 'Failed to register user',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Log validation errors
        logger.error("Validation failed: %s", serializer.errors)
        return JsonResponse({
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Vue de login
class LoginView(APIView):
    permission_classes = [AllowAny]

    # Pour la documentation
    @swagger_auto_schema(request_body=LoginSerializer)
    # Méthode de login
    def post(self, request, *args, **kwargs):
        logger.info("Received data for login: %s", request.data)  # Log input data
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.validated_data
                user_data = UserSerializer(user).data
                tokens = serializer.get_tokens(user)
                
                logger.info("User login successful: %s", user_data)  # Log successful login
                return Response({
                    'message': 'User login successfully',
                    'user': user_data,
                    'access_token': tokens["access"],
                    'refresh': tokens["refresh"]
                }, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error("Error during user login: %s", str(e))  # Log any exceptions
                return Response({
                    'error': 'Login failed',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Log validation errors
        logger.error("Validation failed: %s", serializer.errors)
        return Response({
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
              
              
              
              
# get all forcasseur 

class ListForcasseur(APIView):
    def get(self, request, *args, **kwargs):
        serializer=UserSerializer
        try:
            forcasseurs=User.objects.filter(is_forcasseur=True)           
            list=serializer(forcasseurs,many=True)           
            return Response({"message": "Success", "data": list.data}, status=status.HTTP_200_OK)           
        except:
             return Response({"message": "une erreur est survenue"}, status=status.HTTP_404_NOT_FOUND)
            
        
        