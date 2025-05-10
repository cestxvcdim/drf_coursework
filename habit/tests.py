from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            password='test_password',
        )
        self.client.force_authenticate(user=self.user)

        self.habit1 = Habit.objects.create(
            user=self.user,
            location="test01",
            time="12:46:33",
            action="Открыть окно",
            is_nice=True,
            periodicity="day",
            reward="Игра в приставку",
            complete_time="00:00:30",
            is_public=False
        )

        self.habit2 = Habit.objects.create(
            user=self.user,
            location="test01",
            time="18:04:35",
            action="Зарядка",
            is_nice=False,
            periodicity="day",
            reward="Игра в приставку",
            complete_time="00:02:00",
            is_public=True
        )

    def test_habit_list(self):
        url = reverse('habit:habit-list')
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit2.id,
                    "location": self.habit2.location,
                    "time": self.habit2.time,
                    "action": self.habit2.action,
                    "is_nice": self.habit2.is_nice,
                    "periodicity": self.habit2.periodicity,
                    "reward": self.habit2.reward,
                    "complete_time": self.habit2.complete_time,
                    "is_public": self.habit2.is_public,
                    "user": self.habit2.user.id,
                    "related": self.habit2.related,
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data, result
        )

    def test_habit_detail(self):
        url = reverse('habit:habit-detail', args=[self.habit2.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('action'), "Зарядка"
        )

        self.assertEqual(
            data.get('is_public'), True
        )

    def test_habit_create(self):
        url = reverse('habit:habit-create')
        post_data = {
            "location": "Дом",
            "time": "12:00:00",
            "action": "Полить цветы",
            "is_nice": True,
            "periodicity": "day",
            "reward": "Пицца",
            "complete_time": "00:01:00",
            "is_public": True,
            "user": self.user.id,
        }
        response = self.client.post(url, data=post_data)
        habit = Habit.objects.filter(action="Полить цветы").first()

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertIsNotNone(habit)

        self.assertEqual(
            habit.user, self.user
        )

    def test_habit_create_validation(self):
        url = reverse('habit:habit-create')
        invalid_data1 = {
            "location": "Дом",
            "time": "10:00:00",
            "action": "Неправильная привычка",
            "is_nice": False,
            "periodicity": "day",
            "related": self.habit1.id,
            "reward": "Награда",
            "complete_time": "00:03:00",
            "is_public": True,
            "user": self.user.id,
        }
        invalid_data2 = {
            "location": "Дом",
            "time": "10:00:00",
            "action": "Неправильная привычка",
            "is_nice": False,
            "periodicity": "day",
            "related": self.habit2.id,
            "complete_time": "00:02:00",
            "is_public": True,
            "user": self.user.id,
        }

        response = self.client.post(url, data=invalid_data1)
        response2 = self.client.post(url, data=invalid_data2)
        errors = response.json()
        errors2 = response2.json()

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response2.status_code, status.HTTP_400_BAD_REQUEST
        )

        print(errors, errors2)

        self.assertIn(
            "Время выполнения привычки не должно превышать 0:02:00.", errors["non_field_errors"]
        )
        self.assertIn(
            "Разрешено выбрать либо связанную привычку либо вознаграждение.", errors["non_field_errors"]
        )
        self.assertIn(
            "Можно связывать только полезные привычки с приятными.", errors2["non_field_errors"]
        )

    def test_habit_update(self):
        url = reverse('habit:habit-update', args=[self.habit1.pk])
        updated_data = {
            "location": "Новое место",
            "time": "13:00:00",
            "action": "Новое действие",
            "is_nice": True,
            "periodicity": "2 days",
            "reward": 'Звонок другу',
            "complete_time": "00:00:49",
            "is_public": False,
            "user": self.user.id,
        }
        response = self.client.put(url, updated_data)
        habit = Habit.objects.get(id=self.habit1.id)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            habit.location, "Новое место"
        )

    def test_habit_delete(self):
        url = reverse('habit:habit-delete', args=[self.habit2.id])
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
