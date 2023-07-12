from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import UserProfile
from .serializers import UserProfileSerializer, UserAccountProfileSerialzer
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileView(APIView):
    def get(self, request, format=None):
        user = request.user

        try:
            userProfile = UserProfile.objects.get(user=user)

        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile does not exist."}, status=404)

        serializer = UserAccountProfileSerialzer(instance=user)

        return Response(serializer.data, status=200)


class UserProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        try:
            userProfile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile does not exist."}, status=404)

        serializer = UserProfileSerializer(userProfile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, format=None):
        # Get the user associated with the request
        user = request.user

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile does not exist."}, status=404)

        serializer = UserProfileSerializer(
            profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=400)


class ProfileView(APIView):

    def get(self, request, username, format=None):
        try:
            freelancer = User.objects.filter(username=username).first()
            profile = UserProfile.objects.get(user=username)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAccountProfileSerialzer(instance=freelancer)

        return Response(serializer.data, status=status.HTTP_200_OK)
