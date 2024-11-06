from django.db import models

from users.models import Parieur

# Create your models here.

class Subscription(models.Model):
    amount=models.IntegerField()
    date=models.DateTimeField(null=True, blank=True)
    transaction_id=models.CharField(max_length=255)
    parieur=models.ForeignKey(Parieur,on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')
    