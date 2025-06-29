from django.views import View
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .forms import CustomUserRegistrationForm
from .utils import send_activation_email

User = get_user_model()


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = CustomUserRegistrationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_activation_email(self.request, user)  # вот здесь вызываешь
        return render(self.request, "users/email_confirmation_sent.html")


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, "users/activation_success.html")
        else:
            return render(request, "users/activation_failed.html")


class EmailConfirmationSentView(TemplateView):
    template_name = "users/email_confirmation_sent.html"


class ActivationSuccessView(TemplateView):
    template_name = "users/activation_success.html"


class ActivationFailedView(TemplateView):
    template_name = "users/activation_failed.html"


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"  # по желанию


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = "/users/password-reset/done/"


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = "/users/password-reset/complete/"


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
