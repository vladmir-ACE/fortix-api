from django.urls import path
from .views import (
    AddPronosticView, AddResultatView, DeleteResultatView, JeuxByJourAndCountryAPIView, JourListCreateAPIView, JourRetrieveUpdateDestroyAPIView,
    JeuxListCreateAPIView, JeuxRetrieveUpdateDestroyAPIView, ListPronoByUserAndCountry,
    PronosticListCreateAPIView, ResultatsByDay, ResultatsByDayCountry, StatsForcasseurView, TotalPronosticsForcasseurView,UpdatePronosticView, PronosticListView, PronosticRetrieveUpdateDestroyAPIView,ClientPronosticsTodayView,ClientPronosticsByDay,
    DeletePronosticView,ClientPronosticsByDayAndForcasseur, UpdateResultat, WinningPronostics
)

urlpatterns = [
    # Jour URLs
    path('jours/', JourListCreateAPIView.as_view(), name='jour-list-create'),
    path('jours/<int:pk>/', JourRetrieveUpdateDestroyAPIView.as_view(), name='jour-detail'),

    # Jeux URLs
    path('jeux/', JeuxListCreateAPIView.as_view(), name='jeux-list-create'),
    path('jeux/<int:pk>/', JeuxRetrieveUpdateDestroyAPIView.as_view(), name='jeux-detail'),
    
    #jeux by pays et jours
    path('jeux/<int:jour_id>/<int:pays_id>/', JeuxByJourAndCountryAPIView.as_view(), name='jeux_by_jour_and_country'),

    # Pronostic URLs
    # generics endpoint
    # path('pronostics/', PronosticListCreateAPIView.as_view(), name='pronostic-list-create'),
    # path('pronostics/<int:pk>/', PronosticRetrieveUpdateDestroyAPIView.as_view(), name='pronostic-detail'),
    
    path('add/', AddPronosticView.as_view(), name='add_pronostic'),
    path('update/<int:pronostic_id>/', UpdatePronosticView.as_view(), name='update_pronostic'),
    path('delete/<int:prono_id>/', DeletePronosticView.as_view(), name='delete_pronostic'),
    path('list/', PronosticListView.as_view(), name='list_pronostics'),
    
    path('filter/<int:user_id>/<int:pays_id>/', ListPronoByUserAndCountry.as_view(), name='get_pronostics_by_user_and_country'),
    
    
    # Pronostic des clients 
    path('client/prono/<int:pays_id>/',ClientPronosticsTodayView.as_view(),name="list_of_todays_pronostic_for_client"),
    path('client/prono/<int:jour_id>/<int:pays_id>/',ClientPronosticsByDay.as_view(),name="list_of_pronostics_by_days"),
    
    #Pronostic d'un forcasseur dans la semaine en cours 
    path('client/prono/byforc/<int:pays_id>/<int:user_id>/',ClientPronosticsByDayAndForcasseur.as_view(),name="list_pronostic_by_forcas"),
    
    #PARTIE DES RESULTATS
    path('add/resultat/', AddResultatView.as_view(), name='add_resultats'),
    path('list/resultat/<int:pays_id>/', ResultatsByDay.as_view(), name='list_resultats'),
    path('list/resultat/<int:jour_id>/<int:pays_id>/', ResultatsByDayCountry.as_view(), name='list_resultats_par_jours'),
    path('update/resultat/<int:resultat_id>/', UpdateResultat.as_view(), name='update_resultat'),
    path('delete/resultat/<int:resultat_id>/', DeleteResultatView.as_view(), name='delete_resultat'),
    
    #PARTIE DES PRONOSTICS GAGNANTS
    path('list/wining/<int:pays_id>/', WinningPronostics.as_view(), name='list_prono_gagnants'),
    
    ##PRONOSTICS STATISTICS 
    path('stats/nbre_prono/<int:forcasseur_id>/', TotalPronosticsForcasseurView.as_view(), name='nbre_prono_forc'),
    path('stats/forc/<int:user_id>/', StatsForcasseurView.as_view(), name='stat_forc'),
    
    
]
