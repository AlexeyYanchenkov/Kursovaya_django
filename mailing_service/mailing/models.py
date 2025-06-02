from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailings')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CREATED')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"Рассылка {self.id} - {self.get_status_display()}"

class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ('SUCCESS', 'Успешно'),
        ('FAILURE', 'Ошибка'),
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Попытка {self.mailing_id} - {self.get_status_display()} - {self.attempt_datetime}"

class MessageLog(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    status = models.BooleanField()  # True — успешно, False — ошибка
    timestamp = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)  # ответ от сервера или ошибка

    def __str__(self):
        return f'{self.mailing} - {self.client} - {"OK" if self.status else "FAIL"}'