from rest_framework import serializers
from .models import Jobs, JobBids


class JobsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBids
        fields = ('job', 'bidder', 'bid_amount', 'date_of_bidding')


class JobAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ('free_lancer')
