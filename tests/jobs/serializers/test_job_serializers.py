from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from Account.models import UserProfile
from jobs.serializers import (
    JobsSerializers,
    JobDetailViewSerializer,
    JobAssignSerializer,
    BidSerializer,
)
from jobs.models import Jobs, JobBids

User = get_user_model()


class TestJobSerializer(TestCase):
    def setUp(self) -> None:
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
        self.job1 = Jobs.objects.create(
            title='Test Job',
            description='Testing Job Serializer',
            creator=self.creator1,
            tag=['Testing', 'Django', 'Pytest']
        )
        self.jobBid1 = JobBids.objects.create(
            job=self.job1,
            bidder=self.freelancer1,
            bid_amount=12.00,
            date_of_bidding=timezone.now()
        )

    def test_job_serializer(self):
        data = {
            'title': 'Test Job',
            'description': 'Testing Job Serializer',
            'creator': self.creator1.pk,
            'tag': ['Testing', 'Django', 'Pytest']
        }

        serializer = JobsSerializers(data=data)

        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())

    def test_bid_serializer(self):
        data = {
            'job': self.job1.pk,
            'bidder': self.freelancer1.pk,
            'bid_amount': 12.00,
            'date_of_bidding': timezone.now()
        }

        serializer = BidSerializer(data=data)

        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())

    def test_job_detail_serializer(self):
        expected_data = {
            'title': 'Test Job',
            'description': 'Testing Job Serializer',
            'created_at': timezone.now(),
            'updated_at': None,
            'creator': self.creator1.pk,
            'is_completed': False,
            'completion_date': None,
            'verified': False,
            'date_of_verification': None,
            'tag': ['Testing', 'Django', 'Pytest'],
            'bid': {
                'job': self.job1.pk,
                'bidder': self.freelancer1.pk,
                'bid_amount': 12.00,
                'date_of_bidding': timezone.now()
            }
        }

        serializer = JobDetailViewSerializer(instance=self.job1)
        print(serializer.data)
