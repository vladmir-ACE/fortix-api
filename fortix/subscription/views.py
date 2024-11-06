

# Create your views here.
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Parieur, Subscription
from django.conf import settings
import random
import string

from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils import timezone

# Fonction pour générer un identifiant de transaction unique
def generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def generate_payment_url(request, parieur_id):
    
    print(parieur_id)
    # Récupérer le parieur
    parieur = get_object_or_404(Parieur, id=parieur_id)

    # Générer un transaction_id
    transaction_id = generate_transaction_id()

    # Détails de l'API CinetPay
    url = 'https://api-checkout.cinetpay.com/v2/payment'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "apikey": settings.CINETPAY_API_KEY,
        "site_id": settings.CINETPAY_SITE_ID,
        "transaction_id": transaction_id,
        "amount": 100,  # Montant de l'abonnement, par ex. 100 XOF
        "currency": "XOF",
        "description": "Abonnement parieur",
        "return_url": "https://876b-2c0f-f0f8-836-fd00-45c3-1f24-c978-96ce.ngrok-free.app/subscribe/payment-return/",  # URL de retour après paiement
        "notify_url": "https://876b-2c0f-f0f8-836-fd00-45c3-1f24-c978-96ce.ngrok-free.app/subscribe/payment-notify/",  # URL de notification CinetPay
        "customer_name": parieur.user.first_name,
        "customer_surname": parieur.user.last_name,
        "customer_email": "vladgnouyaro@gmail.com",
        "customer_phone_number": parieur.user.phone_number,
        "customer_address" : "BP 0024",
        "customer_city": "lome",
        "customer_country" : "TG",
        "customer_state" : "TG",
        "customer_zip_code" : "06510", 
        "channels": "ALL",  # Paiement via tous les moyens disponibles
    }

    # Envoyer la requête à CinetPay
    response = requests.post(url, json=payload, headers=headers)
    
    print(response)

    if response.status_code == 200:
        data = response.json()
        # Sauvegarder les informations dans Subscription avant redirection
        Subscription.objects.create(
            parieur=parieur,
            amount=100,  # Montant du paiement
            transaction_id=transaction_id
        )
        # Retourner l'URL de paiement à l'utilisateur
        return JsonResponse({'payment_url': data['data']['payment_url']})

    return JsonResponse({'error': 'Échec de la création du paiement'}, status=400)


@csrf_exempt
def payment_notify(request):
    if request.method == 'POST':
        data = request.json()
        transaction_id = data.get('transaction_id')
        status = data.get('status')

        try:
            # Récupérer l'abonnement via le transaction_id
            subscription = Subscription.objects.get(transaction_id=transaction_id)

            if status == "ACCEPTED":
                # Mise à jour de la souscription
                subscription.date = timezone.now()
                subscription.save()

                # Activer l'abonnement pour le parieur
                parieur = subscription.parieur
                parieur.subscription_active = True
                parieur.subscription_start_date = timezone.now()
                parieur.subscription_end_date = timezone.now() + timedelta(days=30)  # Exemple : abonnement de 30 jours
                parieur.save()
                
            print("Notification traitée avec succès")

            return JsonResponse({"message": "Notification traitée avec succès"})

        except Subscription.DoesNotExist:
            return JsonResponse({"error": "Transaction non trouvée"}, status=404)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



def payment_return(request):
    status = request.GET.get('status')
    
    if status == "ACCEPTED":
        message = "Votre paiement a été effectué avec succès."
    else:
        message = "Votre paiement a échoué. Veuillez réessayer."
        
    print(message)
    
