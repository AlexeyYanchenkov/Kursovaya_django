from django.core.mail import send_mail
from django.utils import timezone
from .models import MessageLog
import logging

logger = logging.getLogger(__name__)

def send_mailing_messages(mailing):
    message = mailing.message
    clients = mailing.clients.all()

    for client in clients:
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=None,
                recipient_list=[client.email],
                fail_silently=False,
            )

            MessageLog.objects.create(
                mailing=mailing,
                client=client,
                status=True,
                response='Success'
            )
            logger.info(f"Successfully sent to {client.email}")

        except Exception as e:
            MessageLog.objects.create(
                mailing=mailing,
                client=client,
                status=False,
                response=str(e)
            )
            logger.error(f"Failed to send to {client.email}: {e}")