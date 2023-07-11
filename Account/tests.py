from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import UserProfileSerializer, UserAccountProfileSerialzer

User = get_user_model()


class TestUserAccountModelCase(TestCase):
    def test_create_user_with_all_required_fields(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
            password='testpassword'
        )

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('testpassword'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_without_required_fields(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                username='',
                first_name='',
                last_name='',
                password='testpassword'
            )

    def test_username_and_email_uniqueness(self):
        User.objects.create_user(
            email='test1@example.com',
            username='testuser1',
            first_name='John',
            last_name='Doe',
            password='testpassword1'
        )

        with self.assertRaisesMessage(ValueError, 'Email already exists'):
            User.objects.create_user(
                email='test1@example.com',
                username='testuser2',
                first_name='Jane',
                last_name='Smith',
                password='testpassword2'
            )

        with self.assertRaisesMessage(ValueError, 'Username already exists'):
            User.objects.create_user(
                email='test2@example.com',
                username='testuser1',
                first_name='Jane',
                last_name='Smith',
                password='testpassword2'
            )

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            first_name='Admin',
            last_name='User',
            password='adminpassword'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.username, 'adminuser')
        self.assertEqual(superuser.first_name, 'Admin')
        self.assertEqual(superuser.last_name, 'User')
        self.assertTrue(superuser.check_password('adminpassword'))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)

    def test_role_field(self):
        profile = UserProfile.objects.create(user=self.user, role='freelancer')
        self.assertEqual(profile.role, 'freelancer')

    def test_optional_fields(self):
        bio = 'This is test for optional fields'
        skills = 'Python, JavaScript, Data Analysis'
        education = 'Bachelor of Science in Computer Science'
        experience = '3 years of experience in web development'

        profile = UserProfile.objects.create(
            user=self.user,
            bio=bio,
            skills=skills,
            education=education,
            experience=experience
        )

        assert profile.bio == bio
        assert profile.skills == skills
        assert profile.education == education
        assert profile.experience == experience


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
