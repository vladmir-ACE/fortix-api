from rest_framework import generics
from .models import Jour, Jeux, Pronostic
from .serializers import JourSerializer, JeuxSerializer, PronosticSerializer

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
    serializer_class = PronosticSerializer

# Vue pour récupérer, mettre à jour et supprimer un Pronostic spécifique
class PronosticRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pronostic.objects.all()
    serializer_class = PronosticSerializer
