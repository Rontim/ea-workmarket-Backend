from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from .permissions import IsCreator, IsFreeLancer, IsFreeLancerOrReadOnly
from .models import Jobs, JobBids
from .serializers import JobsSerializers, BidSerializer, JobAssignSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class IsACreator(BasePermission):
    message = "Job Creation is restricted to only creators"

    def has_object_permission(self, request, view, obj):
        if request.method in ['POST']:
            return False


class JobCreateView(CreateAPIView, IsACreator):
    permission_classes = [IsACreator]
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializers

    def perform_create(self, serializer):

        serializer.save(creator=self.request.user)


class BiddingView(CreateAPIView):
    permission_classes = [IsFreeLancer]
    serializer_class = BidSerializer
    queryset = JobBids.objects.all()

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)


class AssignJobView(UpdateAPIView):
    queryset = Jobs.objects
    serializer_class = JobAssignSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def perform_update(self, serializer):
        serializer.save(free_lancer=self.request.freelancer)


class BidsListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsCreator]
    serializer_class = BidSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return JobBids.objects.filter(job=job_id)


class JobDetailView(RetrieveAPIView):
    serializer_class = JobsSerializers
    queryset = Jobs.objects.all()
