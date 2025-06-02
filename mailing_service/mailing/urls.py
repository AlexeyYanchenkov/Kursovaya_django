from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='mailing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='mailing/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='mailing/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='mailing/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='mailing/password_reset_complete.html'), name='password_reset_complete'),
    path('statistics/', views.user_statistics, name='user_statistics'),
    path('mailing/edit/<int:pk>/', views.edit_mailing, name='edit_mailing'),
    path('mailing/delete/<int:pk>/', views.delete_mailing, name='delete_mailing'),
    path('mailings/', views.mailing_list, name='mailing_list'),
    path('mailing/create/', views.create_mailing, name='create_mailing'),
    path('clients/', views.client_list, name='client_list'),
]