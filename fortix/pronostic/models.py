from django.db import models
from users.models import Country, Forcasseur  # Import du modèle Forcasseur
from datetime import date


# model for jour 
class Jour(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

#model for jeux
class Jeux(models.Model):
    nom = models.CharField(max_length=100)
    jour = models.ForeignKey(Jour, on_delete=models.CASCADE)  # Chaque jeu a un jour spécifique
    heure = models.TimeField()
    pays = models.ForeignKey(Country, on_delete=models.CASCADE)  # Lien avec le pays

    def __str__(self):
        return self.nom
    
#model for pronostics 

class Pronostic(models.Model):
    date = models.DateField(default=date.today)
    # Représente les numéros du pronostic
    banka=models.CharField(max_length=255 ,null=True)
    two=models.CharField(max_length=255,null=True)
    perm=models.CharField(max_length=255,null=True)
    #jeu et forcasseur
    jeu = models.ForeignKey(Jeux, on_delete=models.CASCADE)  # Relation avec Jeux
    forcasseur = models.ForeignKey(Forcasseur, on_delete=models.CASCADE)  # Relation avec Forcasseur (l'auteur du pronostic)

    def __str__(self):
        return f"Pronostic pour {self.jeu.nom} le {self.date} par {self.forcasseur.user.first_name}"
