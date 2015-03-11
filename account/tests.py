import json
from django.test import TestCase
from django.test.client import Client
from auth.models import AuthKey
from auth.auth import get_dict_md5
from erron import errno


class AuthTestCase(TestCase):

    def add_secret(self, data):
        data['key'] = self.key
        data['secret'] = get_dict_md5(data, self.secret_key)
        return data


class RegisterTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        self.key = 'test_key'
        self.secret_key = 'test_secret_key'
        AuthKey(key=self.key, secret=self.secret_key).save()

    def test_register_normal(self):
        response = self.client.post('/account/user/', self.add_secret({
            'username': 'normal_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_register_exist_username(self):
        response = self.client.post('/account/user/', self.add_secret({
            'username': 'exist_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.post('/account/user/', self.add_secret({
            'username': 'exist_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRON_USERNAME_EXIST)

    def test_register_invalid_method(self):
        response = self.client.put('/account/user/', self.add_secret({
            'username': 'exist_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERROR_INVALID_REQUEST_METHOD)

    def test_register_missing_parameter(self):
        response = self.client.post('/account/user/', self.add_secret({
            'username': 'exist_name'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERROR_MISSING_PARAMETER)


class DeleteTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        self.key = 'test_key'
        self.secret_key = 'test_secret_key'
        AuthKey(key=self.key, secret=self.secret_key).save()
        response = self.client.post('/account/user/', self.add_secret({
            'username': 'delete_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_delete_normal(self):
        response = self.client.delete('/account/user/', self.add_secret({
            'username': 'delete_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_delete_non_exist(self):
        response = self.client.delete('/account/user/', self.add_secret({
            'username': 'delete_name_non',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRON_USERNAME_NON_EXIST)

    def test_delete_mismatch(self):
        response = self.client.delete('/account/user/', self.add_secret({
            'username': 'delete_name',
            'password': 'mismatch'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRON_MISMATCH_USERNAME_PASSWORD)


class LoginTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        self.key = 'test_key'
        self.secret_key = 'test_secret_key'
        AuthKey(key=self.key, secret=self.secret_key).save()
        response = self.client.post('/account/user/', self.add_secret({
            'username': 'login_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_login_normal(self):
        response = self.client.post('/account/token/', self.add_secret({
            'username': 'login_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())

    def test_login_non_exist(self):
        response = self.client.post('/account/token/', self.add_secret({
            'username': 'login_name_non_exist',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRON_USERNAME_NON_EXIST)

    def test_login_mismatch_password(self):
        response = self.client.post('/account/token/', self.add_secret({
            'username': 'login_name',
            'password': 'password_mismatch'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRON_MISMATCH_USERNAME_PASSWORD)

    def test_login_multiple(self):
        response = self.client.post('/account/token/', self.add_secret({
            'username': 'login_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())
        token1 = data['token']
        response = self.client.post('/account/token/', self.add_secret({
            'username': 'login_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())
        token2 = data['token']
        self.assertNotEqual(token1, token2)


class LogoutTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        self.key = 'test_key'
        self.secret_key = 'test_secret_key'
        AuthKey(key=self.key, secret=self.secret_key).save()
        response = self.client.post('/account/user/', self.add_secret({
            'username': 'login_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.post('/account/token/', self.add_secret({
            'username': 'login_name',
            'password': 'password'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())
        self.token = data['token']

    def test_logout_normal(self):
        response = self.client.delete('/account/token/', self.add_secret({
            'username': 'login_name',
            'token': self.token}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_logout_invalid_token(self):
        response = self.client.delete('/account/token/', self.add_secret({
            'username': 'login_name',
            'token': 'Invalid token'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRON_MISMATCH_TOKEN)

