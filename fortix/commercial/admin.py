from django.contrib import admin

from .models import Historique, Portefeuille

# Register your models here.


@admin.register(Portefeuille)
class PortefeuilleAdmin(admin.ModelAdmin):
    list_display = ('id', 'commercial','montant','gain')
    search_fields = ('commercial_user__first_name', 'commercial_user__phone_number')



@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'client','comercial','date')
    search_fields = ('commercial_phone_number', 'client_phone_number')
