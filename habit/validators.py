from datetime import timedelta

from rest_framework.serializers import ValidationError


class RelatedOrReward:
    def __call__(self, value):
        if value.get('related') and value.get('reward'):
            raise ValidationError('Разрешено выбрать либо связанную привычку либо вознаграждение.')


class LimitCompleteTime:
    def __init__(self):
        self.max_duration = timedelta(minutes=2)

    def __call__(self, value):
        time = value.get('complete_time')
        if time and time > self.max_duration:
            raise ValidationError(f'Время выполнения привычки не должно превышать {self.max_duration}.')


class RelatedValidator:
    def __call__(self, value):
        rel = value.get('related')
        if rel and not rel.is_nice:
            raise ValidationError('Можно связывать только полезные привычки с приятными.')
