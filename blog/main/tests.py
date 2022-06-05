from django.test import TestCase
from django.test.client import Client


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', {'username': 'admin@admin.ru', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)