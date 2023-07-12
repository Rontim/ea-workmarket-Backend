from django.test import TestCase
from django.contrib.auth import get_user_model
from Account.models import UserAccount


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
