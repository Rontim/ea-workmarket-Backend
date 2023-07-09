from rest_framework import serializers
from .models import Payment, PaypalDetails, MpesaDetails


class PaypalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalDetails
        fields = '__all__'


class MpesaDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaDetails
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    paypal_details = PaypalDetailsSerializer()
    mpesa_details = MpesaDetailsSerializer()

    class Meta:
        model = Payment
        fields = "__all__"

    def create(self, validated_data):
        paypal_details_data = validated_data.pop('paypal_details', None)
        mpesa_details_data = validated_data.pop('mpesa_details', None)

        payment = Payment.objects.create(**validated_data)

        if paypal_details_data:
            PaypalDetails.objects.create(
                payment=payment, **paypal_details_data)

        if mpesa_details_data:
            MpesaDetails.objects.create(payment=payment, **mpesa_details_data)

        return payment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['paypal_details'] = PaypalDetailsSerializer(
            instance.paypal_details).data
        representation['mpesa_details'] = MpesaDetailsSerializer(
            instance.mpesa_details).data
        return representation
