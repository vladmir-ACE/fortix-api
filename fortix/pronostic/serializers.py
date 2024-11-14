from rest_framework import serializers

from users.models import Forcasseur, User

from .models import Jour, Jeux, Pronostic

class JourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jour
        fields = '__all__'

class JeuxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jeux
        fields = '__all__'

class GenericPronosticSerializer(serializers.ModelSerializer):
    forcasseur = serializers.StringRelatedField()  # Affiche le nom du forcasseur en lecture seule

    class Meta:
        model = Pronostic
        fields = '__all__'


# add pronostic serialiser 
class PronosticSerializer(serializers.ModelSerializer):
    jeu_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    banka = serializers.CharField()
    two = serializers.CharField()
    perm = serializers.CharField()

    class Meta:
        model = Pronostic
        fields = ['jeu_id', 'user_id', 'banka','two','perm']

    def create(self, validated_data):
        jeu_id = validated_data.pop('jeu_id')
        user_id = validated_data.pop('user_id')
        
        try:
            jeu = Jeux.objects.get(id=jeu_id)
            forcasseur = Forcasseur.objects.get(user_id=user_id)
        except (Jeux.DoesNotExist, Forcasseur.DoesNotExist) as e:
            raise serializers.ValidationError(f"Invalid jeu_id or user_id: {str(e)}")

        pronostic = Pronostic.objects.create(
            jeu=jeu,
            forcasseur=forcasseur,
            **validated_data
        )
        return pronostic
    
    
    
    
#part for List pronostic serializer 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'country']

# Serializer pour l'objet Forcasseur, incluant les infos de l'objet User
class ForcasseurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Forcasseur
        fields = ['id', 'user', 'total_winnings', 'success_rate']


class ListPronosticSerializer(serializers.ModelSerializer):
    forcasseur = ForcasseurSerializer()  # Inclure le serializer Forcasseur
    jeu = JeuxSerializer()  # Inclure le serializer Jeux

    class Meta:
        model = Pronostic
        fields = ['id', 'date', 'banka','two','perm', 'jeu', 'forcasseur']