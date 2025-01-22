from django.db import models

from users.models import Commercial, User

# Create your models here.

class Portefeuille(models.Model):
    commercial = models.OneToOneField(Commercial, on_delete=models.CASCADE)  # Relation avec Commercial
    montant = models.FloatField(default=0.0)  # Montant du portefeuille
    gain = models.FloatField(default=0.0)  # Montant du portefeuille
    
    def __str__(self):
        return f"Portefeuille de {self.commercial.user.first_name} : {self.montant}XOF"


class Historique(models.Model):
    client = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='historiques_as_client'  # Nom unique pour la relation inversée
    )
    comercial = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='historiques_as_commercial'  # Nom unique pour la relation inversée
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historique: {self.client} - {self.comercial} - {self.date}"
