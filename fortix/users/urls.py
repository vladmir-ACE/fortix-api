from django.urls import path
from .views import ClassementForcasseur, RegisterView, LoginView,ListForcasseur, UpdateUserAvatar

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forcasseur/', ListForcasseur.as_view(), name='list-forcasseur'),
    path('forcasseur/classement/<int:pays_id>/', ClassementForcasseur.as_view(), name='classement-forcasseur'),
    path('avatar/', UpdateUserAvatar.as_view(), name='classement-forcasseur'),
]
