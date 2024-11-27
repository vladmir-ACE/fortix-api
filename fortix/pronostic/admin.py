from django.contrib import admin
from .models import Jour, Jeux, Pronostic

@admin.register(Jour)
class JourAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')  # Affiche l'ID et le nom dans la liste des jours

@admin.register(Jeux)
class JeuxAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'jour', 'heure', 'pays')  # Affiche les informations importantes dans la liste des jeux
    list_filter = ('jour', 'pays')  # Ajoute des filtres pour les champs jour et pays
    search_fields = ('nom',)  # Ajoute un champ de recherche sur le nom du jeu

@admin.register(Pronostic)
class PronosticAdmin(admin.ModelAdmin):
    list_display = ('id', 'jeu', 'forcasseur', 'date', "banka","two","perm","created_at")  # Affiche les informations principales dans la liste des pronostics
    list_filter = ('date', 'jeu')  # Ajoute des filtres sur la date et le jeu
    search_fields = ('jeu__nom', 'forcasseur__user__first_name')  # Ajoute un champ de recherche sur le nom du jeu et le prénom du forcasseur
