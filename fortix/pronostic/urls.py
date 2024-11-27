from django.urls import path
from .views import (
    AddPronosticView, JeuxByJourAndCountryAPIView, JourListCreateAPIView, JourRetrieveUpdateDestroyAPIView,
    JeuxListCreateAPIView, JeuxRetrieveUpdateDestroyAPIView, ListPronoByUserAndCountry,
    PronosticListCreateAPIView, PronosticListView, PronosticRetrieveUpdateDestroyAPIView,ClientPronosticsTodayView,ClientPronosticsByDay
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
    path('list/', PronosticListView.as_view(), name='list_pronostics'),
    
    path('filter/<int:user_id>/<int:pays_id>/', ListPronoByUserAndCountry.as_view(), name='get_pronostics_by_user_and_country'),
    
    
    # Pronostic des clients 
    path('client/prono/<int:pays_id>/',ClientPronosticsTodayView.as_view(),name="list of todays pronostic for client"),
    path('client/prono/<int:jour_id>/<int:pays_id>/',ClientPronosticsByDay.as_view(),name="list of pronostics by days")
    
]
