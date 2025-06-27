from celery import shared_task
from django.utils import timezone
from .models import Mailing
from .services import send_mailing_messages

@shared_task
def send_scheduled_mailings():
    now = timezone.now()
    mailings = Mailing.objects.filter(
        start_datetime__lte=now,
        end_datetime__gte=now,
        is_active=True
    )

    for mailing in mailings:
        send_mailing_messages(mailing)