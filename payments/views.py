import os
import json
import base64
import requests
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Payment, PaypalDetails, MpesaDetails
from django.contrib.auth import get_user_model
User = get_user_model()


CLIENT_ID = os.environ.get('CLIENT_ID')
APP_SECRET = os.environ.get('APP_SECRET')
base_url = os.environ.get('base_url')


@api_view('POST', 'GET')
def PaymentSetupView(request):
    if request.method == 'POST':
        if request.data['type'] == 'paypal':
            pass
        if request.data['type'] == 'mpesa':
            pass

    if request.method == 'GET':
        pass


class PayPalPayment(APIView):

    def post(self, request, format=None):
        auth = base64.b64encode(f'{CLIENT_ID}:{APP_SECRET}'.encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
        }
        data = {
            "grant_type": "client_credentials",
        }
        url = f'{base_url}/v1/oauth2/token'
        response = requests.post(url, headers=headers, data=data)
        access_token = response.json()['access_token']

        amount = request.data['amount']
        freelancer_email = request.data['freelancer']
        url = f'{base_url}/v2/checkout/orders'
        try:
            freelancer = User.objects.get(email=freelancer_email)
        except User.DoesNotExist:
            return Response({'error': 'Freelancer not found'})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "value": str(amount),
                        "currency_code": "USD"
                    },
                    "payee": {
                        "email_address": freelancer.email
                    }
                }
            ],
            'redirect_urls': {
                'return_url': "",
                'cancel_url': "",
            },
        }

        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))

        if response.status_code == 201:
            approve_url = response.json()['links'][1]['href']
            return redirect(approve_url)
        else:
            return Response(status=response.status_code)
