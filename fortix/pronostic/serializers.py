from rest_framework import serializers
from .models import Jour, Jeux, Pronostic

class JourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jour
        fields = '__all__'

class JeuxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jeux
        fields = '__all__'

class PronosticSerializer(serializers.ModelSerializer):
    forcasseur = serializers.StringRelatedField()  # Affiche le nom du forcasseur en lecture seule

    class Meta:
        model = Pronostic
        fields = '__all__'
