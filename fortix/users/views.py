import logging
import cloudinary
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Forcasseur, User
from .serializers import ForcasseurSerializer, RegisterSerializer, LoginSerializer, UserSerializer
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
    def get(self, request,  *args, **kwargs):
        try:
            forcasseurs = Forcasseur.objects.all()
            serializer = ForcasseurSerializer(forcasseurs, many=True)
            return Response({"message": "List forcasseur", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            # Journalisation de l'erreur pour un meilleur suivi
            logger.error(f"Erreur lors de la récupération des forcasseurs : {str(e)}")
            return Response({"message": "Une erreur est survenue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ClassementForcasseur(APIView):
    def get(self, request, pays_id, *args, **kwargs):
        try:
            # Filtrer les forcasseurs en fonction de l'ID du pays
            forcasseurs = Forcasseur.objects.filter(user__country_id=pays_id).order_by('-total_winnings')
            
            # Sérialisation des données
            serializer = ForcasseurSerializer(forcasseurs, many=True)
            
            # Retourner la réponse avec les données triées
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            # En cas d'erreur, retourner un message d'erreur
            return Response({"message": f"Erreur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#classement génerale
        
class ClassementGeneralForcasseur(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Filtrer les forcasseurs en fonction de l'ID du pays
            forcasseurs = Forcasseur.objects.all().order_by('-total_winnings')
            # Sérialisation des données
            serializer = ForcasseurSerializer(forcasseurs, many=True)
            
            # Retourner la réponse avec les données triées
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            # En cas d'erreur, retourner un message d'erreur
            return Response({"message": f"Erreur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
#UPDATE AVATAR DE L'UTILISATEUR
        
class UpdateUserAvatar(APIView):
    def post(self, request):
        # Récupérer l'utilisateur par l'ID fourni
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        # Vérifier si un fichier a été envoyé
        avatar_file = request.FILES.get('avatar')
        if not avatar_file:
            return Response(
                {"message": "Aucune image fournie."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Envoyer l'image sur Cloudinary
            upload_result = cloudinary.uploader.upload(avatar_file, folder="avatars/")
            avatar_url = upload_result.get("secure_url")

            if not avatar_url:
                return Response(
                    {"message": "Échec de l'upload sur Cloudinary."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Mettre à jour l'utilisateur avec l'URL de l'avatar
            user.avatar = avatar_url
            user.save()

            return Response(
                {
                    "message": "Avatar mis à jour avec succès.",
                    "avatar_url": avatar_url,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Une erreur est survenue : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )