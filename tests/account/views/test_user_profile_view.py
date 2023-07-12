from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from Account.models import UserProfile, UserAccount
from Account.views import ProfileView, UserProfileUpdateView, UserProfileView, UserProfileCreateView
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

    def test_user_profile_view(self):
        UserProfile.objects.create(
            user=self.user
        )
        request = self.factory.get(reverse('profile'))

        request.user = self.user

        url = reverse('profile')

        force_authenticate(request, user=self.user)

        response = UserProfileView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_user_profile_create_view_with_valid_data(self):
        url = reverse('profile-create')
        request = self.factory.post(
            url,
            data={
                'user': self.user.pk,
                'role': 'freelancer',
                'bio': 'I am a freelancer with experience in web development.',
                'skills': ['Python', 'JavaScript'],
                'education': 'Testing University',
                'experience': 'Upwork freelancer',
                'address': 'Kenya',
            },
            content_type='application/json'
        )

        request.user = self.user
        force_authenticate(request, user=self.user)
        response = UserProfileCreateView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role'], 'freelancer')

    def test_profile_update_with_valid_data(self):
        UserProfile.objects.create(user=self.user)
        url = reverse('profile-update')
        data = {
            'bio': 'Testing profile update view'
        }

        request = self.factory.patch(
            url, data=data,  content_type='application/json')
        request.user = self.user
        force_authenticate(request, user=self.user)

        response = UserProfileUpdateView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'],
                         'Testing profile update view')

    def test_get_profile_for_existing_user(self):
        UserProfile.objects.create(
            user=self.user,
            role='freelancer',
            bio='I am a freelancer with experience in web development.',
            skills=['Python', 'JavaScript'],
            education='Testing University',
            experience='Upwork freelancer',
            address='Kenya',
        )
        url = reverse('bidders-profile', args=[self.user.pk])
        print(url)
        request = self.factory.get(url)
        request.user = self.user1
        force_authenticate(request, user=self.user1)
        response = ProfileView.as_view()(request, username=self.user.username)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
