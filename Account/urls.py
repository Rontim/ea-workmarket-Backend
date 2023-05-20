from django.urls import path, include
from .views import UserProfileCreateView

urlpatterns = [
    path('profile/', UserProfileCreateView.as_view()),
]
