from django.test import TestCase
from django.test.client import Client
from auth.models import AuthKey
from auth.auth import get_dict_md5


class AccountTestCase(TestCase):

    def setUp(self):
        self.key = 'test_key'
        self.secret_key = 'test_secret_key'
        AuthKey(key=self.key, secret=self.secret_key).save()

    def add_secret(self, data):
        data['key'] = self.key
        data['secret'] = get_dict_md5(data, self.secret_key)
        return data

    def test_register(self):
        client = Client()
        response = client.post('/account/user/', self.add_secret({'username': 'test_name', 'password': 'password'}))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        pass

    def test_logout(self):
        pass
