from django.urls import path
from .views import ClassementForcasseur, ClassementGeneralForcasseur, DashLoginView, RegisterView, LoginView,ListForcasseur, SubscriptionCheck, UpdateUserAvatar,RegisterCommercialView, UserInfoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forcasseur/', ListForcasseur.as_view(), name='list-forcasseur'),
    path('forcasseur/classement/<int:pays_id>/', ClassementForcasseur.as_view(), name='classement-forcasseur'),
    path('forcasseur/classement/', ClassementGeneralForcasseur.as_view(), name='classement-forcasseur'),
    path('avatar/', UpdateUserAvatar.as_view(), name='classement-forcasseur'),
    
    #commercial register 
    path('register/commercial/', RegisterCommercialView.as_view(), name='register_for_commercial'),
    
    #dashboard login 
    path('dashboard/login/', DashLoginView.as_view(), name='dash_login'),
    
    #user info by phone  number
    path('info/<str:user_id>', UserInfoView.as_view(), name='user'),
    
    #check subscription 
    path('checksub/<int:user_id>/', SubscriptionCheck.as_view(), name='check_subscription'),
    
]
