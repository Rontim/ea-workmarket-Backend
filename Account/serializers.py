from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import UserAccount


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = "__all__"


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserAccount
        fields = ('name', 'email')
