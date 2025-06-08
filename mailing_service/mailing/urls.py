from django.urls import path
from . import views


urlpatterns = [
    path('statistics/', views.user_statistics, name='user_statistics'),
    path('edit/<int:pk>/', views.edit_mailing, name='edit_mailing'),
    path('delete/<int:pk>/', views.delete_mailing, name='delete_mailing'),
    path('', views.mailing_list, name='mailing_list'),
    path('create/', views.create_mailing, name='create_mailing'),
    path('clients/', views.client_list, name='client_list'),
]