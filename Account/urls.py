from django.urls import path, include
from .views import UserProfileCreateView, UserProfileUpdateView, UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view()),
    path('profile/create/', UserProfileCreateView.as_view()),
    path('profile/update/', UserProfileUpdateView.as_view()),

]
