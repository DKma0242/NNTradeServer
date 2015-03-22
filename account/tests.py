import json
from django.test import TestCase
from django.test.client import Client
from wrappers.wrapper import get_dict_md5
from errnos import errno


class AuthTestCase(TestCase):

    def add_token(self, data, token):
        data['token'] = get_dict_md5(data, token)
        return data


class RegisterTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_register_normal(self):
        response = self.client.post('/account/user/', {'username': 'normal_name',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_register_exist_username(self):
        response = self.client.post('/account/user/', {'username': 'exist_name',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.post('/account/user/', {'username': 'exist_name',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_USERNAME_EXIST)

    def test_register_invalid_method(self):
        response = self.client.put('/account/user/', {'username': 'exist_name',
                                                      'password': 'password'})
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


class DeleteTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        response = self.client.post('/account/user/', {'username': 'delete_name',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_delete_normal(self):
        response = self.client.delete('/account/user/', {'username': 'delete_name',
                                                         'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_delete_non_exist(self):
        response = self.client.delete('/account/user/', {'username': 'delete_name_non',
                                                         'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_USERNAME_NON_EXIST)

    def test_delete_mismatch(self):
        response = self.client.delete('/account/user/', {'username': 'delete_name',
                                                         'password': 'mismatch'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISMATCH_USERNAME_PASSWORD)


class LoginTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        response = self.client.post('/account/user/', {'username': 'login_name',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_login_normal(self):
        response = self.client.post('/account/token/', {'username': 'login_name',
                                                        'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())

    def test_login_non_exist(self):
        response = self.client.post('/account/token/', {'username': 'login_name_non_exist',
                                                        'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_USERNAME_NON_EXIST)

    def test_login_mismatch_password(self):
        response = self.client.post('/account/token/', {'username': 'login_name',
                                                        'password': 'password_mismatch'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISMATCH_USERNAME_PASSWORD)

    def test_login_multiple(self):
        response = self.client.post('/account/token/', {'username': 'login_name',
                                                        'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())
        token1 = data['token']
        response = self.client.post('/account/token/', {'username': 'login_name',
                                                        'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())
        token2 = data['token']
        self.assertNotEqual(token1, token2)


class LogoutTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
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

    def test_logout_normal(self):
        response = self.client.delete('/account/token/', self.add_token({'username': 'login_name'}, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_logout_missing_parameter(self):
        response = self.client.delete('/account/token/', {'username': 'login_name'}, 'Invalid Token')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISSING_PARAMETER)

    def test_logout_non_exist(self):
        response = self.client.delete('/account/token/', self.add_token({'username': 'non_name'}, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_USERNAME_NON_EXIST)

    def test_logout_no_token(self):
        self.client = Client()
        response = self.client.post('/account/user/', {'username': 'non_login',
                                                       'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.delete('/account/token/', self.add_token({'username': 'non_login'}, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NO_TOKEN)

    def test_logout_invalid_token(self):
        response = self.client.delete('/account/token/', self.add_token({'username': 'login_name'}, 'Invalid Token'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISMATCH_TOKEN)

