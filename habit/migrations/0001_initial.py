# Generated by Django 5.2.1 on 2025-05-10 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "location",
                    models.CharField(max_length=100, verbose_name="место привычки"),
                ),
                (
                    "time",
                    models.DateTimeField(
                        verbose_name="время начала выполнения привычки"
                    ),
                ),
                ("action", models.TextField(verbose_name="действие")),
                ("is_nice", models.BooleanField(verbose_name="приятная привычка?")),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("3 days", "Каждые 3 дня"),
                            ("2 days", "Каждые 2 дня"),
                            ("week", "Каждую неделю"),
                            ("day", "Каждый день"),
                        ],
                        default="day",
                        max_length=6,
                        verbose_name="периодичность",
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="вознаграждение",
                    ),
                ),
                (
                    "complete_time",
                    models.DurationField(verbose_name="время на выполнение привычки"),
                ),
                (
                    "is_public",
                    models.BooleanField(
                        default=False, verbose_name="публичная привычка?"
                    ),
                ),
                (
                    "related",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="related_habit",
                        to="habit.habit",
                        verbose_name="связано с",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "привычка",
                "verbose_name_plural": "привычки",
            },
        ),
    ]
