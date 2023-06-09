from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Jobs


@receiver(post_save, sender=Jobs)
def send_mail_on_create(sender, created, instance):
    if created:
        subject = 'Job Creation Notification'
        recepient = [instance.creator.email]

        context = {'job_title': instance.title}
        html_message = render_to_string(
            'job_creation_email.html', context=context)
        plain_message = strip_tags(html_message)

        send_mail(subject, html_message=html_message,
                  from_email=None, recipient_list=recepient)
