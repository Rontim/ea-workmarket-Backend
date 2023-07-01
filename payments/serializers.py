from rest_framework import serializers
from .models import Payment, PaypalDetails, MpesaDetails


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaypalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalDetails
        fields = '__all__'


class MpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaDetails
        fields = '__all__'
