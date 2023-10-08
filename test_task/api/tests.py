import unittest, requests, random, string, json, asyncio, aiohttp
from httpx import AsyncClient



class TestJWTAuthentication(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://localhost:8000/auth" 
        self.url = 'http://127.0.0.1:8000/api_v1/user/1/visited_domains/'

    def test_is_auth(self):
        """Класс теста авторизации пользователя"""

        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))

        user_credentials = {
            'username': username,
            'password': password
        }


        response = requests.post(f"{self.base_url}/users/", data=user_credentials)
        self.assertEqual(response.status_code, 201)  


        response = requests.post(f"{self.base_url}/jwt/create/", data=user_credentials)
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
        """Проверка того, что не авторизованный пользователь не сможет отправить запрос к эндпоинту"""
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 401)


class TestEndpoint(unittest.TestCase):
    """Класс теста эндпоинтов."""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWN'
                      'jZXNzIiwiZXhwIjoxNjk3NTc4ODkyLCJqdGkiOiJkYzhkMDNlYzAwZjY0NmFm'
                      'YjdjYzQzMDQ5YTAzZWFlNSIsInVzZXJfaWQiOjJ9.sH-nZrUox3cUr7wLzme5'
                      'I5SbEK1NtRkKcvEp96zayPU')

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def test_age_15_create_user(self):
        """Тест создания пользователя по эндпоинту /user"""
        url = f'{self.base_url}/api_v1/user/'
        
        payload = {
            "first_name": "Иван",
            "second_name":"Иванов",
            "patronymic":"Иванович",
            "age":"15",
            "departament":"IT",
            "post":"senior",
            "email":"pochta@gmail.com"
        }

        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)


    def test_age_79_create_user(self):
        """Тест создания пользователя по эндпоинту /user"""
        url = f'{self.base_url}/api_v1/user/'
        
        payload = {
            "first_name": "Иван",
            "second_name":"Иванов",
            "patronymic":"Иванович",
            "age":"79",
            "departament":"IT",
            "post":"senior",
            "email":"pochta@gmail.com"
        }

        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_positive_post_visited_links(self):
        """Тест успешной отправки ссылок на эндпоинт /visited_links."""

        url = f'{self.base_url}/api_v1/user/1/visited_links/'
        payload = {
            'links':[
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

        url = f'{self.base_url}/api_v1/user/1/visited_links/'

        payload = {
            'links': 'http://mail.com/letter/'
        }

        response = requests.post(url, json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_positive_get_visited_domains(self):
        """Тест успешного получения уникальных доменов по эндпоинту /visited_domains."""

        url = 'http://127.0.0.1:8000/api_v1/user/1/visited_domains/'
        
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
        Тест успешного получения уникальных доменов по эндпоинту /visited_domains
        отфильтрованных временными рамками.
        """

        url = f'{self.base_url}/api_v1/user/1/visited_domains?from=1696591785&to=1696608903'
        
        expected_ans = {
            "domains":[],
            "status":"ok"
            }

        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        try:
            actual_response = response.json()
        except json.JSONDecodeError:
            self.fail("Невозможно декодировать JSON из ответа")
        self.assertDictEqual(actual_response, expected_ans)

class RPCTest(unittest.TestCase):
    """Класс для теста RPC эндпоинтов."""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWN'
                      'jZXNzIiwiZXhwIjoxNjk3NTc4ODkyLCJqdGkiOiJkYzhkMDNlYzAwZjY0NmFm'
                      'YjdjYzQzMDQ5YTAzZWFlNSIsInVzZXJfaWQiOjJ9.sH-nZrUox3cUr7wLzme5'
                      'I5SbEK1NtRkKcvEp96zayPU')

        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    async def async_test_rpc_visited_domains(self):
        """
        Тест на асинхронные 50 запросов к эндпоинту /visited_domains.
        """
        headers = self.headers
        url = f'{self.base_url}/api_v1/user/1/visited_domains/'
        async with AsyncClient() as client:
            
            tasks = []

            for _ in range(30):
                task = client.get(url, headers=headers)
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            for response in responses:
                self.assertEqual(response.status_code, 200)

    def test_async_rpc_visited_domains(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait_for(self.async_test_rpc_visited_domains
                                                 (), timeout=30))


    async def async_test_rpc_visited_links(self):
        """
        Тест на асинхронные 30 запросов к эндпоинту /visited_links.
        """
        headers = self.headers
        url = f'{self.base_url}/api_v1/user/1/visited_links/'
        payload = {
            'links': ['https://ya.ru/котики/']
        }
        async with aiohttp.ClientSession() as session:
            tasks = []

            for _ in range(30):
                task = asyncio.ensure_future(self.post_request(session, url, payload, headers))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            for response in responses:
                self.assertEqual(response.status, 200)

    async def post_request(self, session, url, payload, headers):
        async with session.post(url, json=payload, headers=headers) as response:
            return response

    def test_async_rpc_visited_links(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait_for(self.async_test_rpc_visited_links(), timeout=30))

if __name__ == '__main__':
    unittest.main()