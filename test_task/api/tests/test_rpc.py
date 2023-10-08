import unittest
import asyncio
import aiohttp
from httpx import AsyncClient


class RPCTest(unittest.TestCase):
    """Класс для теста RPC эндпоинтов."""

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

    async def async_test_rpc_visited_domains(self):
        """
        Тест на асинхронные 30 запросов к эндпоинту /visited_domains.
        """
        headers = self.headers
        url = f'{self.base_url}/api/v1/user/1/visited_domains/'
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
        loop.run_until_complete(
            asyncio.wait_for(self.async_test_rpc_visited_domains(),
                             timeout=30))

    async def async_test_rpc_visited_links(self):
        """
        Тест на асинхронные 30 запросов к эндпоинту /visited_links.
        """
        headers = self.headers
        url = f'{self.base_url}/api/v1/user/1/visited_links/'
        payload = {
            'links': ['https://ya.ru/котики/']
        }
        async with aiohttp.ClientSession() as session:
            tasks = []

            for _ in range(30):
                task = asyncio.ensure_future(
                    self.post_request(session, url, payload, headers))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            for response in responses:
                self.assertEqual(response.status, 200)

    async def post_request(self, session, url, payload, headers):
        async with session.post(
                               url, json=payload, headers=headers) as response:
            return response

    def test_async_rpc_visited_links(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait_for(self.async_test_rpc_visited_links(), timeout=30))
