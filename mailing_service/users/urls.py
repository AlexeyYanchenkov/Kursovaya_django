from django.urls import path
from .views import (
    RegisterView,
    ActivateView,
    EmailConfirmationSentView,
    ActivationSuccessView,
    ActivationFailedView,
    UserLoginView,
    UserLogoutView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path(
        "email_confirmation_sent/",
        EmailConfirmationSentView.as_view(),
        name="email_confirmation_sent",
    ),
    path(
        "activation_success/",
        ActivationSuccessView.as_view(),
        name="activation_success",
    ),
    path(
        "activation_failed/", ActivationFailedView.as_view(), name="activation_failed"
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("password-reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
