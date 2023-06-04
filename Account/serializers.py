from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
    TokenSerializer,
    TokenCreateSerializer
)

from rest_framework import serializers
from .models import UserAccount, UserProfile


class CustomTokenCreateSerializer(TokenCreateSerializer):
    pass


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
    skills = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = UserProfile
        fields = '__all__'

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


class UserProfileViewSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        role = instance.role

        representation = {}
        user = instance.user
        representation['email'] = user.email
        representation['name'] = user.first_name
        representation['role'] = role
        representation['bio'] = instance.bio

        if role == 'Candidate':
            representation.update({
                'skills': instance.skills,
                'education': instance.education,
                'experience': instance.experience,
                'address': instance.address,
            })

        elif role == 'Employer':
            representation.update({
                'company': instance.company,
                'industry': instance.industry,
                'job_title': instance.job_title,
                'company_location': instance.company_location,
            })

        return representation

    def get_email(self, instance):
        return instance.user.email

    def get_name(self, instance):
        return instance.user.first_name
