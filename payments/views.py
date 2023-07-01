from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .models import Payment, PaypalDetails, MpesaDetails


@api_view('POST', 'GET')
def PaymentSetupView(request):
    if request.method == 'POST':
        if request.data['type'] == 'paypal':
            pass
        if request.data['type'] == 'mpesa':
            pass

    if request.method == 'GET':
        pass
