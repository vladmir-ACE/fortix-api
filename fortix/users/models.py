from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# counrty model 
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nom du pays

    def __str__(self):
        return self.name
    
    
#user model 
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)  # Relation avec la table Pays
    is_forcasseur = models.BooleanField(default=False)
    is_parieur = models.BooleanField(default=False)
    is_commercial = models.BooleanField(default=False)
    is_dashadmin = models.BooleanField(default=False)
    
    avatar=models.CharField(max_length=255,null=True,blank=True)
    


    def __str__(self):
        return self.phone_number

    
## model parieur 
class Parieur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_active = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    def has_active_subscription(self):
        """
        Vérifie si le parieur a un abonnement valide.
        """
        if self.subscription_active and self.subscription_end_date:
            return self.subscription_end_date >= timezone.now()
        return False

#model forcasseur 
class Forcasseur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_winnings = models.FloatField(default=0.0)
    success_rate = models.FloatField(default=0.0)
    subscription_active = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name
    
    def has_active_subscription(self):
        """
        Vérifie si le parieur a un abonnement valide.
        """
        if self.subscription_active and self.subscription_end_date:
            return self.subscription_end_date >= timezone.now()
        return False
    
    
#model commercial 

class Commercial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=25, unique=True,blank=True)
    
    def __str__(self):
        return self.user.phone_number + " " + self.email
