from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from Account.models import UserProfile
from Account.serializers import UserProfileSerializer, UserAccountProfileSerialzer
from Account.views import UserProfileView, UserProfileCreateView, UserProfileUpdateView, ProfileView

User = get_user_model()


class UserProfileTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.client.force_authenticate(user=self.user)

    def test_user_profile_create_view(self):

        url = reverse('profile-create')

        data = {
            'user': self.user.pk,
            'role': 'freelancer',
            'bio': 'I am a freelancer with experience in web development.',
            'skills': ['Python', 'JavaScript'],
            'education': 'Testing University',
            'experience': 'Upwork freelancer',
            'address': 'Kenya',
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_user_profile_invalid_create_view(self):
        url = reverse('profile-create')
        invalid_data = {

        }
        response = self.client.post(url, invalid_data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())

    def test_user_profile_view(self):
        UserProfile.objects.create(
            user=self.user
        )
        url = reverse('profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.pk)

    def test_profile_view(self):
        UserProfile.objects.create(
            user=self.user
        )

        url = reverse('bidders-profile', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)

    def test_user_profile_retrieval_for_non_existing_user(self):
        url = reverse('profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Profile does not exist.')

    def test_user_profile_update_view(self):
        UserProfile.objects.create(
            user=self.user
        )

        url = reverse('profile-update')
        data = {
            'bio': 'Testing profile update'
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserProfile.objects.filter(
            user=self.user, **data).exists())

    def test_unauthorized_access_to_user_profile(self):
        self.client.force_authenticate(user=None)
        url = reverse('profile')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')
