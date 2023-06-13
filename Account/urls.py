from django.urls import path, include
from .views import UserProfileCreateView, UserProfileUpdateView, UserProfileView, ProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view()),
    path('profile/create/', UserProfileCreateView.as_view()),
    path('profile/update/', UserProfileUpdateView.as_view()),
    path('bidder-profile/<str:username>/', ProfileView.as_view())
]
