from rest_framework.response import Response
from rest_framework import generics,status

from users.models import Forcasseur
from .models import Jour, Jeux, Pronostic
from .serializers import GenericPronosticSerializer, JourSerializer, JeuxSerializer, ListPronosticSerializer, PronosticSerializer
from rest_framework.views import APIView
import logging

from rest_framework import serializers

from datetime import timedelta
from django.utils.timezone import now




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
        
        
    
    
## PARTIE DES FORCASSEURS
    
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
                # Extraction du message brut d'erreur
                if isinstance(e.detail, dict):  # Si c'est un dictionnaire
                    error_message = list(e.detail.values())[0][0] if isinstance(list(e.detail.values())[0], list) else list(e.detail.values())[0]
                elif isinstance(e.detail, list):  # Si c'est une liste
                    error_message = e.detail[0]
                else:  # Si c'est une chaîne ou autre
                    error_message = str(e.detail)
                
                logger.error(f"Validation error: {error_message}")
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Extraction des erreurs du serializer pour une réponse simplifiée
        if isinstance(serializer.errors, dict):
            error_message = list(serializer.errors.values())[0][0] if isinstance(list(serializer.errors.values())[0], list) else list(serializer.errors.values())[0]
        else:
            error_message = str(serializer.errors)

        logger.error(f"Invalid data: {error_message}")
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

#list own pronostic by contry 
class ListPronoByUserAndCountry(APIView):
    def get(self,request, user_id, pays_id):
        try:
            # Récupérer tous les pronostics liés au Forcasseur spécifié par user_id
            forcasseur = Forcasseur.objects.get(user_id=user_id)
            
            # Filtrer les pronostics par Forcasseur et par pays
            pronostics = Pronostic.objects.filter(forcasseur=forcasseur, jeu__pays_id=pays_id).order_by('-created_at')
            
            # Sérialiser les pronostics
            serializer = ListPronosticSerializer(pronostics, many=True)
            
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Forcasseur.DoesNotExist:
            return Response({"message": "Forcasseur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        
## PARTIE DES CLIENT

#pronostic de la journée en cours 
class ClientPronosticsTodayView(APIView):
    def get(self, request, pays_id ):
        try:
            # Définir la correspondance des jours
            EN_TO_FR_DAYS = {
                "MONDAY": "LUNDI",
                "TUESDAY": "MARDI",
                "WEDNESDAY": "MERCREDI",
                "THURSDAY": "JEUDI",
                "FRIDAY": "VENDREDI",
                "SATURDAY": "SAMEDI",
                "SUNDAY": "DIMANCHE",
            }

            # Obtenir le jour actuel en français
            current_datetime = now()
            current_day_en = current_datetime.strftime('%A').upper()  # Jour actuel en anglais
            current_day_fr = EN_TO_FR_DAYS.get(current_day_en)  # Traduire en français

            if not current_day_fr:
                return Response({"error": "Impossible de déterminer le jour actuel."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Calculer le début et la fin de la semaine actuelle
            today = current_datetime.date()
            start_of_week = today - timedelta(days=today.weekday())  # Début de la semaine (lundi)
            end_of_week = start_of_week + timedelta(days=6)  # Fin de la semaine (dimanche)


            # Vérifier si pays_id est fourni
            if not pays_id:
                return Response({"error": "Le paramètre pays_id est requis."}, status=status.HTTP_400_BAD_REQUEST)

            # Filtrer les pronostics du jour actuel dans la semaine actuelle et par pays_id
            pronostics_today = Pronostic.objects.filter(
                jeu__jour__nom=current_day_fr,  # Filtrer par jour
                jeu__pays_id=pays_id,          # Filtrer par pays_id
                date__gte=start_of_week,       # Date >= début de la semaine
                date__lte=end_of_week          # Date <= fin de la semaine
            ).select_related('jeu', 'forcasseur').order_by('-created_at')  # Optimisation des requêtes

           # Sérialiser les pronostics
            serializer = ListPronosticSerializer(pronostics_today, many=True)
            
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "une erreur est survenue"}, status=status.HTTP_404_NOT_FOUND)
        
#pronostic d'une journee quelconque de la semaine en cours 
class ClientPronosticsByDay(APIView):
    def get(self, request,jour_id, pays_id ):
        try:
          
            # Obtenir la date actuelle
            current_datetime = now()
           
            # Calculer le début et la fin de la semaine actuelle
            today = current_datetime.date()
            start_of_week = today - timedelta(days=today.weekday())  # Début de la semaine (lundi)
            end_of_week = start_of_week + timedelta(days=6)  # Fin de la semaine (dimanche)

            # Vérifier si pays_id est fourni
            if not pays_id:
                return Response({"error": "Le paramètre pays_id est requis."}, status=status.HTTP_400_BAD_REQUEST)

            # Filtrer les pronostics du jour actuel dans la semaine actuelle et par pays_id
            pronostics_today = Pronostic.objects.filter(
                jeu__jour_id=jour_id,  # Filtrer par jour
                jeu__pays_id=pays_id,          # Filtrer par pays_id
                date__gte=start_of_week,       # Date >= début de la semaine
                date__lte=end_of_week          # Date <= fin de la semaine
            ).select_related('jeu', 'forcasseur').order_by('-created_at')  # Optimisation des requêtes

           # Sérialiser les pronostics
            serializer = ListPronosticSerializer(pronostics_today, many=True)
            
            return Response({"message": "Liste pronostics", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "une erreur est survenue"}, status=status.HTTP_404_NOT_FOUND)
            