
from rest_framework import serializers

from users.serializers import UserSerializer
from users.models import Commercial

from .models import Historique, Portefeuille


class CommercialSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Commercial
        fields=['id','user','email']


class PortefeuilSerializer(serializers.ModelSerializer):
    commercial=CommercialSerializer()
    class Meta:
        model=Portefeuille
        fields =['id','commercial','montant','gain']
        

class HistoriqueSerializer(serializers.ModelSerializer):
    client=UserSerializer()
    comercial=UserSerializer()
    class Meta:
        model = Historique
        fields = ['id', 'client', 'comercial', 'date'] 