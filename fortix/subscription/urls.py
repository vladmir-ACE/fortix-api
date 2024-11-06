from django.urls import path
from . import views

urlpatterns = [
    path('generate-payment/<int:parieur_id>/', views.generate_payment_url, name='generate_payment'),
    path('payment-notify/', views.payment_notify, name='payment_notify'),
    path('payment-return/', views.payment_return, name='payment_return'),
]
