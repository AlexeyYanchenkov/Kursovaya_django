from django import forms
from .models import Mailing

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'clients', 'start_datetime', 'end_datetime']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }