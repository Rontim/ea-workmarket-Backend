from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    TokenSerializer,
    TokenCreateSerializer
)

from rest_framework import serializers
from .models import UserAccount, UserProfile


class CustomTokenSerializer(TokenSerializer):
    email = serializers.EmailField(source="user.email")

    class Meta(TokenSerializer.Meta):
        fields = ("auth_token", "email")


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = "__all__"


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserAccount
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    skills = serializers.ListField(
        child=serializers.CharField(), required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def validate(self, attrs):
        role = attrs.get('role')

        if role == 'freelancer':
            skills = attrs.get('skills')

            if not skills:
                raise serializers.ValidationError(
                    'Skills field is required for freelancers')

        return attrs

    def to_representation(self, instance):

        role = instance.role

        representation = {
            'role': role,
            'bio': instance.bio,
        }

        if role == 'freelancer':
            representation.update({
                'skills': instance.skills,
                'education': instance.education,
                'experience': instance.experience,
                'address': instance.address,

            })

        elif role == 'creator':
            representation.update({
                'company': instance.company,
                'industry': instance.industry,
                'job_title': instance.job_title,
                'company_location': instance.company_location,

            })

        return representation


class UserAccountProfileSerialzer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']
