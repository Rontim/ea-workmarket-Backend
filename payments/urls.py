
from django.urls import path
from .views import PayPalPayment

urlpatterns = [
    path('paypal/payment/', PayPalPayment.as_view()),
]
