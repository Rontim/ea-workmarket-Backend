from Account.models import UserProfile
from jobs.models import Jobs, JobBids
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

        self.creator_profile = UserProfile.objects.create(
            user=self.creator1,
            role='creator',
            bio='Some bio information',
            company='Test Company',
            industry='Test Industry',
            job_title='Testing Job',
            company_location='Nairobi',
        )
        self.freelancer1 = User.objects.create(
            email='freelancer1@example.com',
            username='freelancer1',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.freelancer_profile = UserProfile.objects.create(
            user=self.freelancer1,
            role='freelancer',
            bio='I am a freelancer with experience in web development.',
            skills=['Python', 'JavaScript'],
            education='Testing University',
            experience='Upwork freelancer',
            address='Kenya',
        )
        self.job = Jobs.objects.create(
            title='Test Job',
            description='This is a test job',
            creator=self.creator1
        )

    def test_jobbid_create_valid_data(self):
        bid = JobBids.objects.create(
            job=self.job,
            bidder=self.freelancer1,
            bid_amount=10.00
        )

        self.assertEqual(bid.job, self.job)
        self.assertEqual(bid.bidder, self.freelancer1)
