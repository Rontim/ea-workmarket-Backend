from rest_framework.permissions import BasePermission
from Account.models import UserProfile
import logging

logger = logging.getLogger(__name__)


class IsCreator(BasePermission):
    creator_role = "creator"

    def has_object_permission(self, request, view, obj):
        print('IsCreator permission class is being executed')
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            role = user_profile.role
            print(role)
        except UserProfile.DoesNotExist:
            return False

        return self.creator_role == role


class IsFreeLancer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.freelancer == request.user.profile.role


class IsFreeLancerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.freelancer == request.user.profile.role
