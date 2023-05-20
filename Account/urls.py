from django.urls import path, include
from .views import UserProfileCreateView, UserProfileUpdateView

urlpatterns = [
    path('profile/', UserProfileCreateView.as_view()),
    path('profile/update/', UserProfileUpdateView.as_view()),
]
