from django.urls import path
from .views import (
    MailingListView, ClientListView, MailingCreateView,
    MailingUpdateView, MailingDeleteView, UserStatisticsView, HomeView
)
from . import views

app_name = 'mailing'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('create/', MailingCreateView.as_view(), name='create_mailing'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('statistics/', UserStatisticsView.as_view(), name='user_statistics'),
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
]