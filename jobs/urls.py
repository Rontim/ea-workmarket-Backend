from django.urls import path
from .views import JobCreateView, JobDetailView, BiddingView, BidsListView, AssignJobView

urlpatterns = [
    path('create/', JobCreateView.as_view()),
    path('<int:pk>/detail/', JobDetailView.as_view()),
    path('<int:pk>/assign/', AssignJobView.as_view()),
    path('<int:pk>/bid/', BiddingView.as_view()),
    path('<int:job_id>/bid/list/', BidsListView.as_view()),
]
