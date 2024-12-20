from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Country, Parieur, Forcasseur

User = get_user_model()

# Serializer pour l'inscription
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country_id = serializers.IntegerField(write_only=True, required=False)  # Ajout du champ country_id

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name', 'password', 'is_forcasseur', 'is_parieur', 'country_id','username']

    def create(self, validated_data):
        # Récupérer le country_id depuis les données de la requête
        country_id = validated_data.pop('country_id', None)
        country_obj = None
        
        # Si un ID de pays est fourni, on essaie de récupérer l'objet correspondant
        if country_id:
            try:
                country_obj = Country.objects.get(id=country_id)
            except Country.DoesNotExist:
                raise serializers.ValidationError("Invalid country ID")

        # Créer l'utilisateur
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_forcasseur=validated_data['is_forcasseur'],
            is_parieur=validated_data['is_parieur'],
            country=country_obj  ,# Associer le pays à l'utilisateur
            username=validated_data['username'],
        )

        # Créer un profil Parieur ou Forcasseur selon le rôle de l'utilisateur
        if user.is_parieur:
            Parieur.objects.create(user=user)
        if user.is_forcasseur:
            Forcasseur.objects.create(user=user)

        return user
    
    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

# Serializer pour le login
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = User.objects.filter(phone_number=phone_number).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid phone number or password")

        # Vérifie si l'utilisateur est un parieur et si son abonnement est actif
        # revoir l'abonnement apres 
        # if user.is_parieur:
        #     parieur = Parieur.objects.get(user=user)
        #     if not parieur.has_active_subscription():
        #         raise serializers.ValidationError("Subscription inactive. Please subscribe before logging in.")

        return user

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


# user serializers 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'country_id' , 'avatar','first_name', 'last_name', 'username', 'is_forcasseur', 'is_parieur']
        
class ForcasseurSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Forcasseur
        fields =['id','user','total_winnings','success_rate']