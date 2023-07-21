from rest_framework import serializers
from .models import Jobs, JobBids
from taggit.serializers import TaggitSerializer, TagListSerializerField


class JobsSerializers(TaggitSerializer, serializers.ModelSerializer):
    tag = TagListSerializerField()

    class Meta:
        model = Jobs
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBids
        fields = ['job', 'bidder', 'bid_amount', 'date_of_bidding']


class JobBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBids
        fields = ('bidder', 'bid_amount', 'date_of_bidding')


class JobAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ["free_lancer"]


class JobDetailViewSerializer(serializers.ModelSerializer):
    tag = TagListSerializerField()
    bids = JobBidSerializer(many=True)

    class Meta:
        model = Jobs
        fields = ['title', 'description', 'created_at', 'updated_at', 'creator', 'is_completed', 'completion_date',
                  "verified", 'date_of_verification', 'tag', 'bids']
