from django.urls import path
from .views import (
    JourListCreateAPIView, JourRetrieveUpdateDestroyAPIView,
    JeuxListCreateAPIView, JeuxRetrieveUpdateDestroyAPIView,
    PronosticListCreateAPIView, PronosticRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # Jour URLs
    path('jours/', JourListCreateAPIView.as_view(), name='jour-list-create'),
    path('jours/<int:pk>/', JourRetrieveUpdateDestroyAPIView.as_view(), name='jour-detail'),

    # Jeux URLs
    path('jeux/', JeuxListCreateAPIView.as_view(), name='jeux-list-create'),
    path('jeux/<int:pk>/', JeuxRetrieveUpdateDestroyAPIView.as_view(), name='jeux-detail'),

    # Pronostic URLs
    path('pronostics/', PronosticListCreateAPIView.as_view(), name='pronostic-list-create'),
    path('pronostics/<int:pk>/', PronosticRetrieveUpdateDestroyAPIView.as_view(), name='pronostic-detail'),
]
