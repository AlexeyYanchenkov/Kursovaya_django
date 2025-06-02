from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt

@admin.action(description='Запустить рассылку')
def run_mailing(modeladmin, request, queryset):
    from .utils import send_mailing
    for mailing in queryset:
        send_mailing(mailing)

class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_datetime', 'end_datetime', 'status']
    actions = [run_mailing]


admin.site.register(Mailing, MailingAdmin)
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(MailingAttempt)