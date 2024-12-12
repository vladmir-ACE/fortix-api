from django.test import RequestFactory
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import generics,status

from users.models import Forcasseur
from .models import Jour, Jeux, Pronostic, Resultat
from .serializers import AddResultatSerializer, GenericPronosticSerializer, JourSerializer, JeuxSerializer, ListPronosticSerializer, ListResultatSerializer, PronosticGagnantSerializer, PronosticSerializer
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
            pronostics = Pronostic.objects.all().order_by('-created_at')
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

#update pronostics 

DAYS_INDEX = {
    "LUNDI": 0,
    "MARDI": 1,
    "MERCREDI": 2,
    "JEUDI": 3,
    "VENDREDI": 4,
    "SAMEDI": 5,
    "DIMANCHE": 6,
}

EN_TO_FR_DAYS = {
    "MONDAY": "LUNDI",
    "TUESDAY": "MARDI",
    "WEDNESDAY": "MERCREDI",
    "THURSDAY": "JEUDI",
    "FRIDAY": "VENDREDI",
    "SATURDAY": "SAMEDI",
    "SUNDAY": "DIMANCHE",
}

class UpdatePronosticView(APIView):
    def put(self, request, pronostic_id):
        try:
            # Récupération du pronostic à modifier
            pronostic = Pronostic.objects.get(id=pronostic_id)
        except Pronostic.DoesNotExist:
            return Response({"error": "Pronostic introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # Obtenir la date actuelle
        current_date = now().date()
        
        # Calculer le début et la fin de la semaine actuelle
        start_of_week = current_date - timedelta(days=current_date.weekday())  # Début de la semaine (lundi)
        end_of_week = start_of_week + timedelta(days=6)  # Fin de la semaine (dimanche)

        # Vérifier si la date du pronostic est dans la semaine actuelle
        if not (start_of_week <= pronostic.date <= end_of_week):
            return Response(
                {"error": "Vous ne pouvez modifier ce pronostic car il n'a pas été enregistré dans la semaine actuelle."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Récupération des informations du jeu associé au pronostic
        jeu = pronostic.jeu

        # Récupérer le jour et l'heure actuels
        current_datetime = now()
        current_day = current_datetime.strftime('%A').upper()  # Jour actuel en anglais (majuscule)
        current_time = current_datetime.time()

        # Convertir le jour actuel en français
        current_day_fr = EN_TO_FR_DAYS.get(current_day)

        # Récupérer l'indice des jours pour comparaison
        current_day_index = DAYS_INDEX.get(current_day_fr)
        jeu_day_index = DAYS_INDEX.get(jeu.jour.nom)

        if current_day_index is None or jeu_day_index is None:
            return Response({"error": "Une erreur est survenue avec la conversion des jours."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification 1 : Si le jour du jeu est déjà passé
        if current_day_index > jeu_day_index:
            return Response(
                {"error": f"Le jour du jeu ({jeu.jour.nom}) est déjà passé. Vous ne pouvez pas modifier ce pronostic."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérification 2 : Si le jour est aujourd'hui, comparer l'heure
        if current_day_index == jeu_day_index and current_time > jeu.heure:
            return Response(
                {"error": "L'heure du jeu est déjà passée pour aujourd'hui. Vous ne pouvez pas modifier ce pronostic."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mise à jour des données du pronostic
        pronostic.banka = request.data.get('banka', pronostic.banka)
        pronostic.two = request.data.get('two', pronostic.two)
        pronostic.perm = request.data.get('perm', pronostic.perm)
        pronostic.save()

        # Retourner la réponse en cas de succès
        return Response(
            {"message": "Pronostic mis à jour avec succès.", "data": {
                "id": pronostic.id,
                "banka": pronostic.banka,
                "two": pronostic.two,
                "perm": pronostic.perm,
            }},
            status=status.HTTP_200_OK,
        )
        
#delete pronostics 
class DeletePronosticView(APIView):
    def delete(self, request, prono_id):
        try:
            # Récupérer le pronostic à supprimer
            pronostic = Pronostic.objects.get(id=prono_id)
        except Pronostic.DoesNotExist:
            return Response(
                {"error": "Pronostic introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Suppression du pronostic
        pronostic.delete()

        # Réponse en cas de succès
        return Response(
            {"message": f"Pronostic avec l'ID {prono_id} supprimé avec succès."},
            status=status.HTTP_200_OK
        )

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
            
#pronostic d'une journee quelconque de la semaine en cours 
class ClientPronosticsByDayAndForcasseur(APIView):
    def get(self, request,jour_id, pays_id,user_id ):
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
                forcasseur__user_id=user_id,  # Filtrer par forcasseur
                jeu__pays_id=pays_id,          # Filtrer par pays_id
                date__gte=start_of_week,       # Date >= début de la semaine
                date__lte=end_of_week          # Date <= fin de la semaine
            ).select_related('jeu', 'forcasseur').order_by('-created_at')  # Optimisation des requêtes

           # Sérialiser les pronostics
            serializer = ListPronosticSerializer(pronostics_today, many=True)
            
            return Response({"message": "Liste pronostics", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "une erreur est survenue"}, status=status.HTTP_404_NOT_FOUND)
            
            

#PARIE ADMIN POUR LES RESULTATS
## add
class AddResultatView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddResultatSerializer(data=request.data)

        if serializer.is_valid():
            try:
                 # Enregistrement du résultat
                resultat = serializer.save()
                logger.info(f"Resultat created successfully for jeu_id {request.data['jeu_id']}")

                # Préparation de l'appel interne à WinningPronostics
                jour_id = resultat.jeu.jour.id
                pays_id = resultat.jeu.pays.id
                jeu_id = resultat.jeu.id  # ID du jeu spécifique
                factory = RequestFactory()

                # Construire une requête GET interne pour WinningPronostics
                internal_request = factory.get(
                    reverse('list_prono_gagnants', kwargs={'jour_id': jour_id, 'pays_id': pays_id})
                )

                # Instancier la vue WinningPronostics et appeler la méthode GET
                winning_pronostics_view = WinningPronostics.as_view()
                response = winning_pronostics_view(internal_request, jour_id=jour_id, pays_id=pays_id)

                # Vérifier le statut de la réponse
                if response.status_code != 200:
                    logger.error(f"Error retrieving winning pronostics: {response.data}")
                    return Response(
                        {"error": "Failed to retrieve winning pronostics"},
                        status=response.status_code
                    )

                # Récupération des pronostics gagnants depuis la réponse
                pronostics_gagnants = response.data.get('data', [])
                
                # Filtrer uniquement les pronostics pour le jeu spécifique
                pronostics_gagnants_specifiques = [
                    prono for prono in pronostics_gagnants if prono['jeu']['id'] == jeu_id
                ]

                # Mise à jour des scores des forcasseurs
                for prono in pronostics_gagnants_specifiques:
                    forcasseur_id = prono['forcasseur']['id']
                    points = prono['score']  # Supposons que la vue WinningPronostics renvoie les points
                    if points > 0:
                        forcasseur = Forcasseur.objects.get(id=forcasseur_id)
                        forcasseur.total_winnings += points
                        forcasseur.save()

                return Response({"message": "Resultat created and scores updated successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            
            
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
    
    

##list by days and country

class ResultatsByDay(APIView):
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
            resulats_today = Resultat.objects.filter(
                jeu__jour_id=jour_id,  # Filtrer par jour
                jeu__pays_id=pays_id,          # Filtrer par pays_id
                date__gte=start_of_week,       # Date >= début de la semaine
                date__lte=end_of_week          # Date <= fin de la semaine
            ).select_related('jeu').order_by('-created_at')  # Optimisation des requêtes

            print(resulats_today)
           # Sérialiser les pronostics
            serializer = ListResultatSerializer(resulats_today, many=True)
            
            return Response({"message": "Liste des resulats", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "une erreur est survenue"}, status=status.HTTP_404_NOT_FOUND)
       
## update 
class UpdateResultat(APIView):
    def put(self, request, resultat_id):
        try:
            # Récupération du resultat à modifier
            resultat = Resultat.objects.get(id=resultat_id)
        except Resultat.DoesNotExist:
            return Response({"error": "Resultat introuvable."}, status=status.HTTP_404_NOT_FOUND)

   

        # Mise à jour des données du resultat
        resultat.numbers = request.data.get('numbers', resultat.numbers)
        resultat.win = request.data.get('win', resultat.win)
        resultat.mac = request.data.get('mac', resultat.mac)
        resultat.save()

        # Retourner la réponse en cas de succès
        return Response(
            {"message": "Resultat mis à jour avec succès.", "data": {
                "id": resultat.id,
                "numbers": resultat.numbers,
                "win": resultat.win,
                "mac": resultat.mac,
            }},
            status=status.HTTP_200_OK,
        )
        
##delete resultat
class DeleteResultatView(APIView):
    def delete(self, request, resultat_id):
        try:
            # Récupérer le pronostic à supprimer
            resultat = Resultat.objects.get(id=resultat_id)
        except Resultat.DoesNotExist:
            return Response(
                {"error": "Resultat introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Suppression du pronostic
        resultat.delete()

        # Réponse en cas de succès
        return Response(
            {"message": f"Resultat avec l'ID {resultat_id} supprimé avec succès."},
            status=status.HTTP_200_OK
        )

## pronostics gagnants 
class WinningPronostics(APIView):
    def get(self, request, jour_id, pays_id):
        try:
            # Obtenir la date actuelle et les limites de la semaine
            current_datetime = now()
            today = current_datetime.date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            # Vérification du paramètre pays_id
            if not pays_id:
                return Response({"error": "Le paramètre pays_id est requis."}, status=status.HTTP_400_BAD_REQUEST)

            # Récupération des résultats filtrés
            resultats = Resultat.objects.filter(
                jeu__jour_id=jour_id,
                jeu__pays_id=pays_id,
                date__gte=start_of_week,
                date__lte=end_of_week
            ).select_related('jeu')
            
            if not resultats.exists():
                return Response({"message": "Pas encore de résultats", "data": []}, status=status.HTTP_200_OK)

            # Organisation des résultats par jeu
            results_by_game = {}
            for result in resultats:
                if result.jeu.id not in results_by_game:
                    results_by_game[result.jeu.id] = []
                results_by_game[result.jeu.id].append({
                    'type': result.type,
                    'numbers': result.numbers,
                    'win': result.win,
                    'mac': result.mac
                })

            # Récupération des pronostics et filtrage en fonction des résultats
            pronostics = Pronostic.objects.filter(
                jeu__jour_id=jour_id,
                jeu__pays_id=pays_id,
                date__gte=start_of_week,
                date__lte=end_of_week
            ).select_related('jeu', 'forcasseur')

            filtered_pronostics = []
            for pronostic in pronostics:
                matching_results = results_by_game.get(pronostic.jeu.id, [])
                if self.has_winning_numbers(pronostic, matching_results):
                    filtered_pronostics.append(pronostic)

            # Sérialisation des pronostics filtrés
            serializer = PronosticGagnantSerializer(filtered_pronostics, many=True, context={'results': results_by_game})
            return Response({"message": "Pronostics gagnants", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": "Une erreur est survenue", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def has_winning_numbers(self, pronostic, results):
        """
        Vérifie si le pronostic correspond à l'un des résultats disponibles.
        """
        banka = set(pronostic.banka.split('-')) if pronostic.banka else set()
        two = set(pronostic.two.split('-')) if pronostic.two else set()
        perm = set(pronostic.perm.split('-')) if pronostic.perm else set()

        for result in results:
            if result['type'] == 'SIMPLE':
                result_numbers = set(result['numbers'].split('-'))
            elif result['type'] == 'DOUBLE':
                result_numbers = set(result['win'].split('-')) | set(result['mac'].split('-'))
            else:
                continue

            # Vérifiez si au moins une correspondance existe
            if (banka & result_numbers) or (two & result_numbers) or (perm & result_numbers):
                return True
        return False

        
### STATISTIQUES 
##NBR DE PRONOSTIC D'UN FORCASSEUR 

class TotalPronosticsForcasseurView(APIView):
    def get(self, request, forcasseur_id, *args, **kwargs):
        try:
            # Vérifier si le forcasseur existe
            forcasseur = Forcasseur.objects.filter(id=forcasseur_id).first()
            if not forcasseur:
                return Response({"message": "Forcasseur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            # Calculer le nombre total de pronostics
            total_pronostics = Pronostic.objects.filter(forcasseur_id=forcasseur_id).count()

            return Response({
                "message": "Succès",
                "data": {
                    "forcasseur_id": forcasseur_id,
                    "total_pronostics": total_pronostics
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Gestion des erreurs
            return Response({"message": f"Une erreur est survenue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



## nbre prono and score of forc 

class StatsForcasseurView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            # Vérifier si le forcasseur existe
            forcasseur = Forcasseur.objects.filter(user_id=user_id).first()
            if not forcasseur:
                return Response({"message": "Forcasseur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            # Calculer le nombre total de pronostics
            total_pronostics = Pronostic.objects.filter(forcasseur_id=forcasseur.id).count()

            return Response({
                "message": "Succès",
                "data": {
                    "forcasseur_id": forcasseur.id,
                    "score":forcasseur.total_winnings,
                    "total_pronostics": total_pronostics
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Gestion des erreurs
            return Response({"message": f"Une erreur est survenue : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

