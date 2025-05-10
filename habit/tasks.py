from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from habit.models import Habit
from habit.services import send_tg_message, is_today


@shared_task
def remind_habits():
    now_date = now().date()
    now_time = now().time()

    for habit in Habit.objects.all():
        print(f"check {habit.id}")
        habit_time = timedelta(
            hours=habit.time.hour,
            minutes=habit.time.minute,
            seconds=habit.time.second
        ).total_seconds()
        print(habit_time)

        current_time = timedelta(
            hours=now_time.hour,
            minutes=now_time.minute,
            seconds=now_time.second
        ).total_seconds()
        print(current_time)
        print(abs(habit_time - current_time))

        if abs(habit_time - current_time) < 300:
            if is_today(now_date, habit.user.date_joined.date(), habit.periodicity) and habit.user.tg_chat_id:
                text = f"Напоминание: пора выполнить привычку '{habit.action}' в {habit.location} в {habit.time}."
                print(habit.user.tg_chat_id)
                send_tg_message(habit.user.tg_chat_id, text)
