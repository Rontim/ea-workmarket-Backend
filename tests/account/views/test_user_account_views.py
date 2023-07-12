from django.urls import reverse
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

    def test_user_profile_create_view(self):
        user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

        self.client.force_authenticate(user=user)

        url = reverse('profile-create')

        data = {
            'user': user.pk,
            'role': 'freelancer',
            'bio': 'I am a freelancer with experience in web development.',
            'skills': ['Python', 'JavaScript'],
            'education': 'Testing University',
            'experience': 'Upwork freelancer',
            'address': 'Kenya',
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_user_profile_view(self):
        user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

        self.client.force_authenticate(user=user)
        url = reverse('profile')
        request = self.factory.get(url)
        response = UserProfileView.as_view()(request)
        print(response.status_code)
