from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UsersTestCase(APITestCase):

    def test_user_register(self):
        url = reverse('users:register')
        post_data = {
            "email": "test@example.com",
            "password": "test_password",
            "password_confirm": "test_password",
            "tg_chat_id": 3711894620
        }
        response = self.client.post(url, data=post_data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            data.get('email'), 'test@example.com'
        )
