from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save
from taggit.managers import TaggableManager

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
    date_of_verification = models.DateTimeField(null=True, blank=True)
    tag = TaggableManager()

    def __str__(self):
        return self.title


class JobBids(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(decimal_places=2, max_digits=10)
    date_of_bidding = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Bid by {self.bidder.username} on Job {self.job.title}'


@receiver(post_save, sender=Jobs)
def send_mail_on_create(sender, created, instance, *args, **kwargs):
    if created:
        print("Job created")
        subject = 'Job Creation Notification'
        recipient = [instance.creator.email]

        context = {
            'job_title': instance.title,
            'job_url': f'http://127.0.0.1:8000/job/{instance.id}/detail/'
        }
        template = 'email/job_creation_email.html'
        html_message = render_to_string(
            template_name=template, context=context)
        plain_message = strip_tags(html_message)

        send_mail(subject, message=plain_message,
                  from_email=None, html_message=html_message, recipient_list=recipient)
        print('email sent')


@receiver(post_save, sender=JobBids)
def new_bidding_email(sender, created, instance, *args, **kwargs):
    if created:
        subject = 'New Bidding'
        recipient = [instance.job.creator.email]

        context = {
            'bidder': instance.bidder,
            'bid_amount': instance.bid_amount,
            'bid_time': instance.date_of_bidding,
            'job_title': instance.job.title,
            'assign_url': f'http://127.0.0.1:8000/job/{instance.id}/assign/',
            'profile_url': f'http://127.0.0.1:8000/bidder-profile/{instance.bidder.username}/'
        }
        template = 'email/job_bid_email.html'
        html_message = render_to_string(
            template_name=template, context=context)
        plain_message = strip_tags(html_message)

        send_mail(subject, message=plain_message,
                  from_email=None, html_message=html_message, recipient_list=recipient)


@receiver(post_save, sender=Jobs)
def assign_email(sender, created, instance, *args, **kwargs):
    if instance.free_lancer:
        subject = 'Job Assignment'
        recipient = [instance.creator.email]
        context = {
            'job_title': instance.title,
            'bidder_name': instance.free_lancer.get_full_name(),
            'bidder_email': instance.free_lancer.email,
            'bidder_rate': instance.free_lancer.rate,
        }

        template = 'email/job_assign_email.html'
        html_message = render_to_string(
            template_name=template, context=context)
        plain_message = strip_tags(html_message)

        send_mail(subject, message=plain_message,
                  from_email=None, html_message=html_message, recipient_list=recipient)
