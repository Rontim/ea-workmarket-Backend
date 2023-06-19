
from datetime import datetime
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from .permissions import IsCreator, IsFreeLancer, IsFreeLancerOrReadOnly
from Account.models import UserProfile
from .models import Jobs, JobBids
from .serializers import JobsSerializers, BidSerializer, JobAssignSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class JobCreateView(views.APIView):

    def post(self, request, format=None):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            role = user_profile.role
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile does not exist"})

        if role != 'creator':
            return Response({"detail": "Job creation is restricted to Job creators"}, status=402)

        serializer = JobsSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BiddingView(CreateAPIView):
    permission_classes = [IsFreeLancer]
    serializer_class = BidSerializer
    queryset = JobBids.objects.all()

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)


class AssignJobView(views.APIView):

    def patch(self, request, pk, format=None):
        freelancer = request.data.get('freelancer')
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            role = user_profile.role
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile does not exist"})

        if role != 'creator':
            return Response({"detail": "Assigning jobs is restricted to Job creators"}, status=403)

        try:
            job = Jobs.objects.get(id=pk)
            freelancer = User.objects.get(username=freelancer)
        except Jobs.DoesNotExist or User.DoesNotExist:
            return Response({"detail": "Job does not exist"})

        if job.creator != request.user:
            return Response({"detail": "Only the job owner can assign this job"}, status=402)

        serializer = JobsSerializers(job, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(free_lancer=freelancer)
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class BidsListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsCreator]
    serializer_class = BidSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return JobBids.objects.filter(job=job_id)


class JobDetailView(RetrieveAPIView):
    serializer_class = JobsSerializers
    queryset = Jobs.objects.all()


class MarkJobComplitionView(views.APIView):
    def patch(self, request, job_id, format=None):
        try:
            job = Jobs.objects.get(id=job_id)
        except Jobs.DoesNotExist:
            return Response({"detail": "Job does not exist"})

        job.is_completed = not job.is_completed

        if job.is_completed:
            job.completion_date = datetime.now()

        else:
            job.completion_date = None

        job.save()

        return Response({"detail": "Job complition status updated"})


class JobVerificationView(views.APIView):
    def patch(self, request, job_id, format=None):
        try:
            job = Jobs.objects.get(id=job_id)
        except Jobs.DoesNotExist:
            return Response({"detail": "Job does not exist"})

        job.verified = not job.verified

        if job.verified:
            job.date_of_verification = datetime.now()

        else:
            job.verified = None

        job.save()

        return Response({"detail": "Verification status updated"})
