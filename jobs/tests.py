from datetime import datetime

import pytz
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from Account.models import UserProfile
from jobs.serializers import (
    JobsSerializers,
    JobDetailViewSerializer,
    JobAssignSerializer,
    BidSerializer, JobBidSerializer,

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
        self.freelancer2 = User.objects.create(
            email='freelancer2@example.com',
            username='freelancer2',
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
        self.jobBid2 = JobBids.objects.create(
            job=self.job1,
            bidder=self.freelancer2,
            bid_amount=12.50,
            date_of_bidding=timezone.now()
        )

    def test_job_detail_serializer(self):
        expected_data = {
            'title': 'Test Job',
            'description': 'Testing Job Serializer',
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'creator': self.creator1.pk,
            'is_completed': False,
            'completion_date': None,
            'verified': False,
            'date_of_verification': None,
            'tag': ['Testing', 'Django', 'Pytest'],
            'bids': [
                {
                    'job': self.job1.pk,
                    'bidder': self.freelancer1.pk,
                    'bid_amount': 12.00,
                    'date_of_bidding': timezone.now()
                },
                {
                    'job': self.job1.pk,
                    'bidder': self.freelancer2.pk,
                    'bid_amount': 12.50,
                    'date_of_bidding': timezone.now()
                }
            ]
        }

        self.job1.updated_at = None  # Set 'updated_at' to None for the test
        self.job1.save()  # Save the Jobs object after modifying it
        serializer = JobDetailViewSerializer(self.job1)

        # Convert timestamps in expected_data to datetime.datetime objects with timezone information (UTC)
        expected_data['created_at'] = expected_data['created_at'].astimezone(pytz.utc)
        expected_data['updated_at'] = expected_data['updated_at'].astimezone(pytz.utc)
        for bid_data in expected_data['bids']:
            bid_data['date_of_bidding'] = bid_data['date_of_bidding'].astimezone(pytz.utc)

        # Convert timestamps in the serialized data to datetime.datetime objects with timezone information (UTC)
        serializer_data = serializer.data
        serializer_data['created_at'] = datetime.fromisoformat(serializer_data['created_at']).astimezone(
            pytz.utc)
        serializer_data['updated_at'] = datetime.fromisoformat(serializer_data['updated_at']).astimezone(
            pytz.utc)
        for bid_data in serializer_data['bids']:
            bid_data['date_of_bidding'] = datetime.fromisoformat(bid_data['date_of_bidding']).astimezone(
                pytz.utc)

        # print('expected data: {}'.format(expected_data))
        print(serializer.data)
        # self.assertEqual(serializer.data, expected_data)
