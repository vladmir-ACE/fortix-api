from rest_framework.response import Response
from rest_framework import generics,status

from users.models import Forcasseur
from .models import Jour, Jeux, Pronostic
from .serializers import GenericPronosticSerializer, JourSerializer, JeuxSerializer, ListPronosticSerializer, PronosticSerializer
from rest_framework.views import APIView
import logging

from rest_framework import serializers




# Configure the logger
logger = logging.getLogger(__name__)

# Vue pour lister et créer des Jours
class JourListCreateAPIView(generics.ListCreateAPIView):
    queryset = Jour.objects.all()
    serializer_class = JourSerializer

# Vue pour récupérer, mettre à jour et supprimer un Jour spécifique
class JourRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jour.objects.all()
    serializer_class = JourSerializer

# Vue pour lister et créer des Jeux
class JeuxListCreateAPIView(generics.ListCreateAPIView):
    queryset = Jeux.objects.all()
    serializer_class = JeuxSerializer

# Vue pour récupérer, mettre à jour et supprimer un Jeux spécifique
class JeuxRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jeux.objects.all()
    serializer_class = JeuxSerializer

# Vue pour lister et créer des Pronostics
class PronosticListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pronostic.objects.all()
    serializer_class = GenericPronosticSerializer

# Vue pour récupérer, mettre à jour et supprimer un Pronostic spécifique
class PronosticRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pronostic.objects.all()
    serializer_class = GenericPronosticSerializer


# recuperer les jeux par id des pays et jours 
class JeuxByJourAndCountryAPIView(APIView):
    def get(self, request, jour_id, pays_id):
        jeux = Jeux.objects.filter(jour_id=jour_id, pays_id=pays_id)
        serializer = JeuxSerializer(jeux, many=True)
        
        response_data = {
            "message": "Liste des jeux pour le jour et pays spécifiés",
            "data": serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
# add pronostics 
class AddPronosticView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PronosticSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                pronostic = serializer.save()
                logger.info(f"Pronostic created successfully for jeu_id {request.data['jeu_id']} by user_id {request.data['user_id']}")
                return Response({"message": "Pronostic created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                logger.error(f"Validation error: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.error(f"Invalid data: {serializer.errors}")
        return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
# list all pronostics 
class PronosticListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            pronostics = Pronostic.objects.all()
            serializer = ListPronosticSerializer(pronostics, many=True)
            logger.info("Pronostics retrieved successfully.")
            return Response({"message": "Pronostics retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving pronostics: {str(e)}")
            return Response({"error": "An error occurred while retrieving pronostics"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
#list own pronostic by contry 
class ListPronoByUserAndCountry(APIView):
    def get(self,request, user_id, pays_id):
        try:
            # Récupérer tous les pronostics liés au Forcasseur spécifié par user_id
            forcasseur = Forcasseur.objects.get(user_id=user_id)
            
            # Filtrer les pronostics par Forcasseur et par pays
            pronostics = Pronostic.objects.filter(forcasseur=forcasseur, jeu__pays_id=pays_id)
            
            # Sérialiser les pronostics
            serializer = ListPronosticSerializer(pronostics, many=True)
            
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Forcasseur.DoesNotExist:
            return Response({"message": "Forcasseur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
