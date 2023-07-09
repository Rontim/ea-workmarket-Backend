import os
import json
import base64
import requests
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Payment, PaypalDetails
from django.contrib.auth import get_user_model
User = get_user_model()


CLIENT_ID = os.environ.get('CLIENT_ID')
APP_SECRET = os.environ.get('APP_SECRET')
base_url = os.environ.get('base_url')


class PayPalPayment(APIView):
    order_id = ''

    def post(self, request, format=None):
        access_token = self.get_access_token()

        if not access_token:
            return Response({'error': 'Failed to obtain access token'}, status=500)

        amount = request.data.get('amount')
        freelancer_email = request.data.get('freelancer')

        try:
            freelancer = User.objects.get(email=freelancer_email)
        except User.DoesNotExist:
            return Response({'error': 'Freelancer not found'}, status=404)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'amount': {
                        'value': str(amount),
                        'currency_code': 'USD'
                    },
                    'payee': {
                        'email_address': freelancer.email
                    }
                }
            ],
            'redirect_urls': {
                'return_url': 'YOUR_RETURN_URL',
                'cancel_url': 'YOUR_CANCEL_URL',
            },
        }

        response = requests.post(
            f'{base_url}/v2/checkout/orders', headers=headers, data=payload)

        if response.status_code == 201:
            approve_url = response.json()['links'][1]['href']
            self.order_id = response.json()['id']

            return redirect(approve_url)
        else:
            return Response(status=response.status_code)

    def get_access_token(self):
        auth = base64.b64encode(f'{CLIENT_ID}:{APP_SECRET}'.encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
        }
        data = {
            'grant_type': 'client_credentials',
        }
        url = f'{base_url}/v1/oauth2/token'
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json().get('access_token')

        return None

    def capture_payment(self):
        access_token = self.get_access_token()

        url = f'{base_url}/v2/checkout/orders/{self.order_id}/capture'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            captured_payment = response.json()
            return captured_payment
        else:

            return None


class PayPalReturn(APIView):
    def get(self, request):
        captured_payment = PayPalPayment.capture_payment()

        if captured_payment:
            capture_id = captured_payment['purchase_units'][0]['payments']['captures'][0]['id']
            status = captured_payment['purchase_units'][0]['payments']['captures'][0]['status']
            amount = captured_payment['purchase_units'][0]['payments']['captures'][0]['amount']['value']
            currency = captured_payment['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
            payment = Payment.objects.filter(order_id=capture_id).first()

            if not payment:
                payment = Payment.objects.create(
                    order_id=capture_id, user=request.user, amount=amount, currency=currency)

            payment.save()

            paypal_details = payment.paypal_details
            if not paypal_details:
                paypal_details = PaypalDetails.objects.create(
                    payment=payment, paypal_transaction_id=capture_id, status=status)
            else:
                paypal_details.paypal_transaction_id = capture_id
                paypal_details.status = status

            paypal_details.save()

            return Response({'success': 'Payment Successful'})

        return Response({'error': ''})
