
from datetime import date, datetime,timedelta
from rest_framework import serializers
from django.utils.timezone import now, make_aware

from users.models import Forcasseur, User

from .models import Jour, Jeux, Pronostic, Resultat

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

# Dictionnaire pour convertir les jours en français en indices (lundi = 0, mardi = 1, ...)
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

class PronosticSerializer(serializers.ModelSerializer):
    jeu_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    banka = serializers.CharField(required=False, allow_blank=True)
    two = serializers.CharField(required=False, allow_blank=True)
    perm = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Pronostic
        fields = ['jeu_id', 'user_id', 'banka', 'two', 'perm']

    def create(self, validated_data):
        jeu_id = validated_data.pop('jeu_id')
        user_id = validated_data.pop('user_id')

        # Récupérer le jeu et le forcasseur
        try:
            jeu = Jeux.objects.get(id=jeu_id)
            forcasseur = Forcasseur.objects.get(user_id=user_id)
        except (Jeux.DoesNotExist, Forcasseur.DoesNotExist) as e:
            raise serializers.ValidationError(f"ID de jeu ou ID d'utilisateur invalide : {str(e)}")

        # Récupérer le jour actuel et l'heure actuelle
        current_datetime = now()
        current_day = current_datetime.strftime('%A').upper()  # Jour actuel en anglais (majuscule)
        current_time = current_datetime.time()

        # Convertir le jour actuel en français
        current_day_fr = EN_TO_FR_DAYS.get(current_day)

        # Récupérer l'indice des jours pour comparaison
        current_day_index = DAYS_INDEX.get(current_day_fr)
        jeu_day_index = DAYS_INDEX.get(jeu.jour.nom)

        if current_day_index is None or jeu_day_index is None:
            raise serializers.ValidationError("Une erreur est survenue avec la conversion des jours.")

        # Vérification 1 : Si le jour du jeu est déjà passé
        if current_day_index > jeu_day_index:
            raise serializers.ValidationError(f"Le jour du jeu ({jeu.jour.nom}) est déjà passé. Vous ne pouvez pas créer de pronostic.")

        # Vérification 2 : Si le jour est aujourd'hui, comparer l'heure
        if current_day_index == jeu_day_index and current_time > jeu.heure:
            raise serializers.ValidationError(
                "L'heure du jeu est déjà passée pour aujourd'hui. Vous ne pouvez pas créer de pronostic."
            )

        # Vérification 3 : Pas de pronostic multiple pour le même jeu dans la semaine
        today = current_datetime.date()
        start_of_week = today - timedelta(days=today.weekday())  # Début de la semaine (lundi)

        existing_pronostic = Pronostic.objects.filter(
            forcasseur=forcasseur,
            jeu=jeu,
            date__gte=start_of_week,
            date__lte=today
        ).exists()

        if existing_pronostic:
            raise serializers.ValidationError(
                "Un pronostic pour ce jeu a déjà été enregistré cette semaine."
            )

        # Création du pronostic
        pronostic = Pronostic.objects.create(
            jeu=jeu,
            forcasseur=forcasseur,
            **validated_data
        )
        return pronostic

    
#update pronostics serializer

    
    
    
#part for List pronostic serializer 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'country_id']

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
        

#serializer for resultat

class AddResultatSerializer(serializers.ModelSerializer):
    jeu_id = serializers.IntegerField(write_only=True)
    type = serializers.CharField(write_only=True)
    numbers = serializers.CharField(required=False, allow_blank=True)
    win = serializers.CharField(required=False, allow_blank=True)
    mac = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model=Resultat  
        fields = ['jeu_id', 'type', 'numbers', 'win', 'mac']
        
    def create(self, validated_data):
        jeu_id = validated_data.pop('jeu_id')
       
        # Récupérer le jeu 
        try:
            jeu = Jeux.objects.get(id=jeu_id)
            
        except (Jeux.DoesNotExist) as e:
            raise serializers.ValidationError(f"ID de jeu  invalide : {str(e)}")

        # Récupérer le jour actuel et l'heure actuelle
        current_datetime = now()
        current_day = current_datetime.strftime('%A').upper()  # Jour actuel en anglais (majuscule)
        current_time = current_datetime.time()

        # Convertir le jour actuel en français
        current_day_fr = EN_TO_FR_DAYS.get(current_day)

        # Récupérer l'indice des jours pour comparaison
        current_day_index = DAYS_INDEX.get(current_day_fr)
        jeu_day_index = DAYS_INDEX.get(jeu.jour.nom)

        if current_day_index is None or jeu_day_index is None:
            raise serializers.ValidationError("Une erreur est survenue avec la conversion des jours.")


        # Vérification 3 : Pas de resultat multiple pour le même jeu dans la semaine
        today = current_datetime.date()
        start_of_week = today - timedelta(days=today.weekday())  # Début de la semaine (lundi)

        existing_resultat = Resultat.objects.filter(
            jeu=jeu,
            date__gte=start_of_week,
            date__lte=today
        ).exists()

        if existing_resultat:
            raise serializers.ValidationError(
                "Un resultat pour ce jeu a déjà été enregistré cette semaine."
            )

        # Création du pronostic
        resultat = Resultat.objects.create(
            jeu=jeu,
            **validated_data
        )
        return resultat
    
    
        


class ListResultatSerializer(serializers.ModelSerializer):
       
    jeu = JeuxSerializer()  # Inclure le serializer Jeux

    class Meta:
        model = Resultat
        fields = ['id', 'date','type', 'numbers','win','mac', 'jeu',]
        
#pronostics gagnants 

class PronosticGagnantSerializer(serializers.ModelSerializer):
    jeu = JeuxSerializer()  # Sérialisation du jeu
    forcasseur = ForcasseurSerializer()  # Sérialisation du forcasseur
    wining_numbers = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = Pronostic
        fields = ['id', 'date', 'banka', 'two', 'perm', 'jeu', 'forcasseur', 'wining_numbers','score']

    def get_wining_numbers(self, obj):
        # Récupérer les résultats associés au jeu du pronostic
        results = self.context.get('results', {}).get(obj.jeu.id, [])
        winning_numbers = set()

        for result in results:
            if result['type'] == 'SIMPLE':
                result_numbers = set(result['numbers'].split('-'))
            elif result['type'] == 'DOUBLE':
                result_numbers = set(result['win'].split('-')) | set(result['mac'].split('-'))
            else:
                continue

            # Vérifiez les correspondances
            banka = set(obj.banka.split('-')) if obj.banka else set()
            two = set(obj.two.split('-')) if obj.two else set()
            perm = set(obj.perm.split('-')) if obj.perm else set()

            winning_numbers |= (banka & result_numbers)
            winning_numbers |= (two & result_numbers)
            winning_numbers |= (perm & result_numbers)

        # Retourner les numéros gagnants formatés avec "-"
        return '-'.join(sorted(winning_numbers))
    
    def get_score(self, obj):
        # Récupérer les résultats associés au jeu du pronostic
        results = self.context.get('results', {}).get(obj.jeu.id, [])
        score = 0
        banka_found = False
        two_found = False

        for result in results:
            if result['type'] == 'SIMPLE':
                result_numbers = set(result['numbers'].split('-'))
            elif result['type'] == 'DOUBLE':
                result_numbers = set(result['win'].split('-')) | set(result['mac'].split('-'))
            else:
                continue

            # Vérifiez les correspondances
            banka = set(obj.banka.split('-')) if obj.banka else set()
            two = set(obj.two.split('-')) if obj.two else set()

            # Marquer comme trouvé si correspondance avec les résultats
            if banka & result_numbers:
                banka_found = True
            if two <= result_numbers:
                two_found = True

        # Calculer le score en fonction des correspondances
        if banka_found and two_found:
            score = 25  # Si les deux sont trouvés
        elif banka_found:
            score = 15  # Si seul le banka est trouvé
        elif two_found:
            score = 10  # Si seul le two est trouvé

        return score