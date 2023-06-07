from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Jobs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_jobs')
    free_lancer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='assigned_jobs', blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    date_of_verification = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class JobBids(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(decimal_places=2, max_digits=10)
    date_of_bidding = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f'Bid by {self.bidder.username} on Job {self.job.title}'
