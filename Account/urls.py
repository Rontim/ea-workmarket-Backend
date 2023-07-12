from django.urls import path, include
from .views import UserProfileCreateView, UserProfileUpdateView, UserProfileView, ProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/create/', UserProfileCreateView.as_view(), name='profile-create'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('bidder-profile/<str:username>/',
         ProfileView.as_view(), name='bidders-profile')
]
