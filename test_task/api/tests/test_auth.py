import random
import requests
import string
import unittest
import os
# import django

# os.environ['DJANGO_SETTINGS_MODULE'] = 'test_task.settings_test'
# django.setup()


class TestJWTAuthentication(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://localhost:8000/auth"
        self.url = 'http://127.0.0.1:8000/api/v1/user/1/visited_domains/'

    def test_is_auth(self):
        """Класс теста авторизации пользователя"""

        username = ''.join(random.choices(string.ascii_letters + string.digits,
                                          k=10))
        password = ''.join(random.choices(
            string.ascii_letters + string.digits + string.punctuation,
            k=12))

        user_credentials = {
            'username': username,
            'password': password
        }

        response = requests.post(f"{self.base_url}/users/",
                                 data=user_credentials)
        self.assertEqual(response.status_code, 201)

        response = requests.post(f"{self.base_url}/jwt/create/",
                                 data=user_credentials)
        self.assertEqual(response.status_code, 200)
        token = response.json().get('access')

        self.assertIsNotNone(token)

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{self.base_url}/users/me/", headers=headers)

        self.assertEqual(response.status_code, 200)

        user_info = response.json()
        self.assertEqual(user_info['username'], user_credentials['username'])

        responce = requests.get(self.url, headers=headers)
        self.assertEqual(responce.status_code, 200)

    def test_not_is_auth(self):
        """
        Проверка того, что не авторизованный пользователь не сможет
        отправить запрос к эндпоинту
        """
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
