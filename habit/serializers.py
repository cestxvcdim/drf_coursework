from rest_framework import serializers

from habit.models import Habit
from habit.validators import RelatedValidator, RelatedOrReward, LimitCompleteTime


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [RelatedValidator(), RelatedOrReward(), LimitCompleteTime()]
