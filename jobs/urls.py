from django.urls import path
from .views import JobCreateView, JobDetailView, BiddingView, BidsListView, AssignJobView, MarkJobComplitionView, JobVerificationView

urlpatterns = [
    path('create/', JobCreateView.as_view()),
    path('<int:pk>/detail/', JobDetailView.as_view()),
    path('<int:pk>/assign/', AssignJobView.as_view()),
    path('<int:pk>/bid/', BiddingView.as_view()),
    path('<int:job_id>/bid/list/', BidsListView.as_view()),
    path('jobs/<int:job_id>/mark-completed/',
         MarkJobComplitionView.as_view(), name='mark-job-completed'),
    path('jobs/<int:job_id>/verify/',
         JobVerificationView.as_view(), name='verify-job'),

]
