from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.conf import settings

from .forms import CustomUserRegistrationForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Активируем после подтверждения email
            user.save()

            current_site = get_current_site(request)
            subject = 'Подтверждение регистрации'
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return render(request, 'users/email_confirmation_sent.html')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'users/activation_success.html')
    else:
        return render(request, 'users/activation_failed.html')

def email_confirmation_sent(request):
    return render(request, 'users/email_confirmation_sent.html')

def activation_success(request):
    return render(request, 'users/activation_success.html')

def activation_failed(request):
    return render(request, 'users/activation_failed.html')