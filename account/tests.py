import json
import hashlib
from django.test import TestCase
from django.test.client import Client
from errnos import errno


class RegisterTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_normal(self):
        response = self.client.post('/account/user/', {'username': 'normal_name',
                                                       'password': hashlib.md5('password').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('user_id' in data.keys())

    def test_register_exist_username(self):
        response = self.client.post('/account/user/', {'username': 'exist_name',
                                                       'password': hashlib.md5('password').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.post('/account/user/', {'username': 'exist_name',
                                                       'password': hashlib.md5('password').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_USERNAME_EXIST)

    def test_register_invalid_method(self):
        response = self.client.put('/account/user/', {'username': 'exist_name',
                                                      'password': hashlib.md5('password').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_INVALID_REQUEST_METHOD)

    def test_register_missing_parameter(self):
        response = self.client.post('/account/user/', {'username': 'exist_name'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISSING_PARAMETER)


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        response = self.client.post('/account/user/', {'username': 'login_name',
                                                       'password': hashlib.md5('password').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_login_normal(self):
        response = self.client.post('/account/login/', {'username': 'login_name',
                                                        'password': hashlib.md5('password').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('user_id' in data.keys())

    def test_login_non_exist(self):
        response = self.client.post('/account/login/', {'username': 'login_name_non_exist',
                                                        'password': hashlib.md5('password').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_USERNAME_NON_EXIST)

    def test_login_mismatch_password(self):
        response = self.client.post('/account/login/', {'username': 'login_name',
                                                        'password': hashlib.md5('password_mismatch').hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISMATCH_USERNAME_PASSWORD)
