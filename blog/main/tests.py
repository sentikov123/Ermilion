from django.test import TestCase
from django.test.client import Client

from .models import User


# Create your tests here.
class ModelTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    # def test_model_data(self):
    #     username = User.get_username_by_id(1)
    #     print('username', username)
    #     self.assertEqual(username, 'admin')
    #

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', {'username': 'admin@admin.ru', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)
