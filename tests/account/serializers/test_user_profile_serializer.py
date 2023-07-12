from django.test import TestCase
from django.contrib.auth import get_user_model
from Account.models import UserProfile
from Account.serializers import UserProfileSerializer, UserAccountProfileSerialzer

User = get_user_model()


class UserProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

    def test_valid_freelancer_serializer(self):
        data = {
            'user': self.user.pk,
            'role': 'freelancer',
            'bio': 'I am a freelancer with experience in web development.',
            'skills': ['Python', 'JavaScript'],
            'education': 'Testing University',
            'experience': 'Upwork freelancer',
            'address': 'Kenya',
        }
        serializer = UserProfileSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_invalid_freelancer_serializer(self):
        data = {
            'user': self.user.pk,
            'role': 'freelancer',
            'bio': 'I am a freelancer without skills.',
        }
        serializer = UserProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_user_account_profile_serializer(self):
        profile_creator = UserProfile.objects.create(
            user=self.user,
            role='creator',
            bio='Some bio information',
            company='Test Company',
            industry='Test Industry',
            job_title='Testing Job',
            company_location='Nairobi',
        )
        serializer = UserAccountProfileSerialzer(instance=self.user)
        expected_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'profile': {
                'role': 'creator',
                'bio': 'Some bio information',
                'company': 'Test Company',
                'industry': 'Test Industry',
                'job_title': 'Testing Job',
                'company_location': 'Nairobi',
            }
        }

        self.assertEqual(serializer.data, expected_data)
