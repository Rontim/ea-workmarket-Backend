from Account.models import UserProfile
from jobs.models import Jobs
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import force_authenticate

User = get_user_model()


class JobModelTest(TestCase):
    def setUp(self):
        self.creator1 = User.objects.create(
            email='creator1@example.com',
            username='creator1',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

    def test_job_create_valid_data(self):
        jobs = Jobs.objects.create(
            title='Test Job',
            description='This is a test job',
            creator=self.creator1
        )

        self.assertEqual(jobs.title, 'Test Job')
        self.assertEqual(jobs.description, 'This is a test job')
        self.assertEqual(jobs.creator, self.creator1)
