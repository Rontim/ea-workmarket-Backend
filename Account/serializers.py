from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import UserAccount, UserProfile


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = "__all__"


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserAccount
        fields = ('name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("address", "country", "city", "birthdate", "bio")
