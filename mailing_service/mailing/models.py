from django.db import models
from users.models import CustomUser  # Кастомная модель пользователя


class Client(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject

    class Meta:
        permissions = [
            ("can_view_all_messages", "Может просматривать все сообщения"),
        ]


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "Создана"),
        ("STARTED", "Запущена"),
        ("FINISHED", "Завершена"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="mailings"
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="CREATED")
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='mailings')
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"Рассылка {self.id} - {self.get_status_display()}"

    class Meta:
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ("SUCCESS", "Успешно"),
        ("FAILURE", "Ошибка"),
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Попытка {self.mailing_id} - {self.get_status_display()} - {self.timestamp}"


class MessageLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.BooleanField()  # True — успешно, False — ошибка
    timestamp = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.mailing} - {self.client} - {"OK" if self.status else "FAIL"}'
