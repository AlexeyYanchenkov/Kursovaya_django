from django import forms
from .models import Mailing, Message, Client


class MailingForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Mailing
        fields = ["message", "clients", "start_datetime", "end_datetime"]
        widgets = {
            'message': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
