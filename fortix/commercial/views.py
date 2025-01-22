from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from users.serializers import UserSerializer

from .serializers import HistoriqueSerializer, PortefeuilSerializer
from users.models import User,Parieur,Forcasseur,Commercial
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Historique, Portefeuille
# Create your views here.

#Abonnement  de compte parieur ou forcasseur

class ActiveUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request,user_id,user_com_id):
        user = get_object_or_404(User, id=user_id)
        
        user_com=get_object_or_404(User, id=user_com_id)
        
        if user.is_parieur:
            # activer ou mettre a jour l'abonnement du parieur
            parieur=get_object_or_404(Parieur, user=user)
            parieur.subscription_active=True
            parieur.subscription_start_date=timezone.now()
            parieur.subscription_end_date=timezone.now()+timezone.timedelta(days=30)
            parieur.save()
            
            # prlever 1000f et ajoute le gain de 200 f dans le portefeuille du commercial 
            commercial=get_object_or_404(Commercial, user=user_com)
            portefeuille=get_object_or_404(Portefeuille, commercial=commercial)
            
            # veifie si le solde du portefeuille est suffisant
            if portefeuille.montant<1000.0:
                return JsonResponse({'message': ' votre solde insufficant pour valider le compte'}, status=400)
            
            portefeuille.montant-=1000.0
            portefeuille.gain+=200.0
            portefeuille.save()
            
            #ajout dans la table historique 
            Historique.objects.create(client=user,comercial=user_com)
            
            
        if user.is_forcasseur:
            forcasseur=get_object_or_404(Forcasseur, user=user)
            forcasseur.subscription_active=True
            forcasseur.subscription_start_date=timezone.now()
            forcasseur.subscription_end_date=timezone.now()+timezone.timedelta(days=30)
            forcasseur.save()
            
            # prlever 1000f dans le portefeuille du commercial 
            commercial=get_object_or_404(Commercial, user=user_com)
            portefeuille=get_object_or_404(Portefeuille, commercial=commercial)
            
            # veifie si le solde du portefeuille est suffisant
            if portefeuille.montant<1000.0:
                return JsonResponse({'message': ' votre solde insufficant pour valider le compte'}, status=400)
            
            portefeuille.montant-=1000.0
            portefeuille.gain+=200.0
            portefeuille.save()
            
            #ajout dans la table historique 
            Historique.objects.create(client=user,comercial=user_com)
        
        return JsonResponse({'message': 'User acount activated successfully'}, status=200)

#Portefeuille d'un commercial

class getPortefeuilleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,user_id):
        user = get_object_or_404(User, id=user_id)
        
        commercial=get_object_or_404(Commercial, user=user)
        portefeuille=get_object_or_404(Portefeuille, commercial=commercial)
        
        return JsonResponse({'montant': portefeuille.montant,'gain':portefeuille.gain}, status=200)
    
#Tous les portefeuilles des commerciaux
class getAllPortefeuilleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        portefeuilles = Portefeuille.objects.all()
        serializer=PortefeuilSerializer(portefeuilles,many=True)
        return JsonResponse({'data':serializer.data,'message':'ListePortefeuille'}, status=HTTP_200_OK)
       
#update le montant d'un portefeuille 
class updatePortefeuilleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pt_id):
        portefeuille = get_object_or_404(Portefeuille, id=pt_id)
        montant = request.data.get('montant')
        portefeuille.montant = montant
        portefeuille.save()
        return JsonResponse({'message': 'Portefeuille updated successfully'}, status=200)
        

# get historique for a commercial
class getHistoriqueView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        historiques = Historique.objects.filter(comercial=user).order_by('-date')
        serializer = HistoriqueSerializer(historiques, many=True)  # Sérialisez les objets Historique
        return JsonResponse({'data':serializer.data,'mesage':'ListeHistorique'}, status=HTTP_200_OK)
        
# get commercial by country id 
class getCommercialByCountryView(APIView):
    def get(self, request, country_id):
        users = User.objects.filter(country_id=country_id, is_commercial=True)
        serializer = UserSerializer(users, many=True)
        return JsonResponse({'data':serializer.data,'message':'ListeCommercial'}, status=HTTP_200_OK)
        

