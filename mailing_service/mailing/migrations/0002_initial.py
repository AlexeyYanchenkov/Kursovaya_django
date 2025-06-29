# Generated by Django 5.1.7 on 2025-06-24 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mailing", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="mailing",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mailings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="mailingattempt",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mailing.client"
            ),
        ),
        migrations.AddField(
            model_name="mailingattempt",
            name="mailing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mailing.mailing"
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mailing.message"
            ),
        ),
        migrations.AddField(
            model_name="messagelog",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mailing.client"
            ),
        ),
        migrations.AddField(
            model_name="messagelog",
            name="mailing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mailing.mailing"
            ),
        ),
    ]
