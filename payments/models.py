from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()


class Payment(models.Model):
    pass


class PaypalDetails(models.Model):
    pass


class MpesaDetails(models.Model):
    pass
