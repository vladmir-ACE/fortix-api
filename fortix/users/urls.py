from django.urls import path
from .views import RegisterView, LoginView,ListForcasseur

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forcasseur/', ListForcasseur.as_view(), name='list-forcasseur'),
]
