from django.core.management.base import BaseCommand
from django.utils import timezone
from mailing.models import Mailing
from mailing.services import send_mailing_messages

class Command(BaseCommand):
    help = 'Send active mailings manually'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        mailings = Mailing.objects.filter(
            start_datetime__lte=now,
            end_datetime__gte=now,
            is_active=True
        )

        if not mailings.exists():
            self.stdout.write(self.style.WARNING('No active mailings to process.'))
            return

        for mailing in mailings:
            try:
                self.stdout.write(f"Processing mailing: {mailing}")
                send_mailing_messages(mailing)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error with mailing {mailing}: {str(e)}"))