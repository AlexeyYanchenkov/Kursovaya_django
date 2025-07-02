from django.core.mail import send_mail
from .models import MailingAttempt
from django.utils import timezone


def send_mailing(mailing):

    mailing.status = "STARTED"
    mailing.save()

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[client.email],
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                status="SUCCESS",
                server_response="Message sent successfully.",
                timestamp=timezone.now(),
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                client=client,
                status="FAILURE",
                server_response=str(e),
                timestamp=timezone.now(),
            )
