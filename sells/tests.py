import json
from django.test import TestCase
from django.test.client import Client
from wrappers.filter import get_dict_md5


class AuthTestCase(TestCase):

    def add_token(self, data, token):
        data['token'] = get_dict_md5(data, token)
        return data

    def login_test_user(self):
        response = self.client.post('/account/user/', {'username': 'login_name',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.post('/account/token/', {'username': 'login_name',
                                                        'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())
        self.token = data['token']


class NewSellPostTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_new_sell_post_normal(self):
        self.login_test_user()
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())

    def test_empty_allowed_field(self):
        self.login_test_user()
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())