from django.urls import path
from .views import ActiveUserView, getAllPortefeuilleView, getCommercialByCountryView, getHistoriqueView, getPortefeuilleView, updatePortefeuilleView

urlpatterns = [
    #path to activate user abonnement
    path('active_acount/<int:user_id>/<int:user_com_id>/', ActiveUserView.as_view(), name='active_user_acount'),
    
    #path to get a commercial portefeuille
    path('portefeuille/<int:user_id>/', getPortefeuilleView.as_view(), name='get_portefeuille'),
    
    #path to list all portefeuille 
    path('portefeuille/all/', getAllPortefeuilleView.as_view(), name='get__all_portefeuilles'),
    
    #update portefeuille montant 
    path('portefeuille/update/<int:pt_id>/', updatePortefeuilleView.as_view(), name='update_portefeuille'),
    
    
    #path historique for commercial 
    path('historique/<int:user_id>/', getHistoriqueView.as_view(), name='get_historiques'),
    
    
    #path get commercial by country id
    path('country/<int:country_id>/', getCommercialByCountryView.as_view(), name='get_commercial_by_country'),
    
   
]
