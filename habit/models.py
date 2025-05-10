from django.core.exceptions import ValidationError
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    PERIODICITY = {
        ('day', 'Каждый день'),
        ('2 days', 'Каждые 2 дня'),
        ('3 days', 'Каждые 3 дня'),
        ('week', 'Каждую неделю'),
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    location = models.CharField(max_length=100, verbose_name='место привычки')
    time = models.TimeField(verbose_name='время начала выполнения привычки')
    action = models.TextField(verbose_name='действие')

    is_nice = models.BooleanField(verbose_name='приятная привычка?')
    related = models.ForeignKey(
        'self', on_delete=models.SET_NULL, **NULLABLE, related_name='related_habit', verbose_name='связанная привычка'
    )
    periodicity = models.CharField(choices=PERIODICITY, max_length=6, default='day', verbose_name='периодичность')

    reward = models.CharField(max_length=100, **NULLABLE, verbose_name='вознаграждение')
    complete_time = models.DurationField(verbose_name='время на выполнение привычки')
    is_public = models.BooleanField(default=False, verbose_name='публичная привычка?')

    def __str__(self):
        return f'{self.user.email} - {self.action[:20]}'

    def clean(self):
        if self.related and not self.related.is_nice:
            raise ValidationError('Можно связывать только полезные привычки с приятными.')

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
