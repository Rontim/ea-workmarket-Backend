from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from Account.serializers import UserAccountProfileSerialzer
from .models import UserProfile, UserAccount
from .views import ProfileView, UserProfileView, UserProfileCreateView, UserProfileUpdateView
from rest_framework.test import force_authenticate
from rest_framework import status


class UserProfileViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserAccount.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.user1 = UserAccount.objects.create(
            email='test1@example.com',
            username='testuser1',
            password='testpassword',
            first_name='Jane',
            last_name='Doe',
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            role='freelancer',
            bio='I am a freelancer with experience in web development.',
            skills=['Python', 'JavaScript'],
            education='Testing University',
            experience='Upwork freelancer',
            address='Kenya',
        )

    def test_get_profile_for_existing_user(self):
        url = reverse('bidders-profile', args=[self.user.pk])
        print(url)
        request = self.factory.get(url)
        request.user = self.user1
        force_authenticate(request, user=self.user1)
        response = ProfileView.as_view()(request, username=self.user.username)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # self.assertEqual(response.data, serializer.data)

    def test_get_profile_for_non_existing_profile(self):
        url = reverse('bidders-profile', args=[self.user1.pk])
        request = self.factory.get(url)
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = ProfileView.as_view()(request, username=self.user1.username)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data, {'detail': 'Profile does not exist'}
        )
