from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            serializer.save(user=user)

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
