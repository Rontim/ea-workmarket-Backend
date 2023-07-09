from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment ID: {self.id}"


class PaypalDetails(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    paypal_transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"PaypalDetails ID: {self.id}"


class MpesaDetails(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    mpesa_transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"MpesaDetails ID: {self.id}"
