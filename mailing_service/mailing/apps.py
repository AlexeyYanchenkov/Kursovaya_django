from django.apps import AppConfig
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        import mailing.tasks