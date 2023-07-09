
from django.urls import path
from .views import PayPalPayment, PayPalReturn

urlpatterns = [
    path('paypal/', PayPalPayment.as_view()),
    path('paypal/return/', PayPalReturn.as_view())
]
