import requests
import json
import unittest


class TestEndpoint(unittest.TestCase):
    """Класс теста эндпоинтов."""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = (
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWN'
            'jZXNzIiwiZXhwIjoxNjk3NTc4ODkyLCJqdGkiOiJkYzhkMDNlYzAwZjY0NmFm'
            'YjdjYzQzMDQ5YTAzZWFlNSIsInVzZXJfaWQiOjJ9.sH-nZrUox3cUr7wLzme5'
            'I5SbEK1NtRkKcvEp96zayPU'
            )

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def test_age_15_create_user(self):
        """Тест создания пользователя по эндпоинту /user"""
        url = f'{self.base_url}/api/v1/user/'

        payload = {
            "first_name": "Иван",
            "second_name": "Иванов",
            "patronymic": "Иванович",
            "age": "15",
            "departament": "IT",
            "post": "senior",
            "email": "pochta@gmail.com"
        }

        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_age_79_create_user(self):
        """Тест создания пользователя по эндпоинту /user"""
        url = f'{self.base_url}/api/v1/user/'

        payload = {
            "first_name": "Иван",
            "second_name": "Иванов",
            "patronymic": "Иванович",
            "age": "79",
            "departament": "IT",
            "post": "senior",
            "email": "pochta@gmail.com"
        }

        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_positive_post_visited_links(self):
        """Тест успешной отправки ссылок на эндпоинт /visited_links."""

        url = f'{self.base_url}/api/v1/user/1/visited_links/'
        payload = {
            'links': [
                'http://mail.com/letter/',
                'http://vk.com/messenger/',
                'https://github.com/KorotkovED/',
                'http://vk.com/friends/',
                'https://github.com/MIZ/'
            ]
        }

        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_negative_post_visited_link(self):
        """Тест не успешной отправки ссылок на эндпоинт /visited_links."""

        url = f'{self.base_url}/api/v1/user/1/visited_links/'

        payload = {
            'links': 'http://mail.com/letter/'
        }

        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_positive_get_visited_domains(self):
        """
        Тест успешного получения уникальных доменов
        по эндпоинту /visited_domains.
        """

        url = 'http://127.0.0.1:8000/api/v1/user/1/visited_domains/'

        expected_ans = {
            'domains': [
                'mail.ru',
                'ya.ru',
                'sberbank',
                'mail.com',
                'vk.com',
                'github.com'
            ],
            'status': 'ok'
        }

        response = requests.get(url, headers=self.headers)
        try:
            actual_response = response.json()
        except json.JSONDecodeError:
            self.fail("Невозможно декодировать JSON из ответа")

        self.assertDictEqual(actual_response, expected_ans)
        self.assertEqual(response.status_code, 200)

    def test_positive_get_visited_domains_time(self):
        """
        Тест успешного получения уникальных доменов
        по эндпоинту /visited_domains
        отфильтрованных временными рамками.
        """

        url = f'{self.base_url}/api/v1/user/1/visited_domains?from=1696591785&to=1696608903'

        expected_ans = {
            "domains": [],
            "status": "ok"
            }

        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        try:
            actual_response = response.json()
        except json.JSONDecodeError:
            self.fail("Невозможно декодировать JSON из ответа")
        self.assertDictEqual(actual_response, expected_ans)


if __name__ == '__main__':
    unittest.main()
