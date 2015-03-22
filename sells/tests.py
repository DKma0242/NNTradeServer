import json
from django.test import TestCase
from django.test.client import Client
from wrappers.wrapper import get_dict_md5
from errnos import errno


class AuthTestCase(TestCase):

    def add_token(self, data, token):
        data['token'] = get_dict_md5(data, token)
        return data

    def login_test_user(self, username, password):
        response = self.client.post('/account/user/', {'username': username,
                                                       'password': password})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.post('/account/token/', {'username': username,
                                                        'password': password})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('token' in data.keys())
        self.token = data['token']


class NewSellPostTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_new_sell_post_normal(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())

    def test_empty_allowed_field(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())


class UpdateSellPostTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_update_post_normal(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())
        post_id = data['id']
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'login_name',
                'title': 'New Title',
                'description': 'New description',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_update_allow_empty(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())
        post_id = data['id']
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'login_name',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_update_not_exist(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())
        post_id = data['id'] + 100
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'login_name',
                'title': 'New Title',
                'description': 'New description',
            }, self.token))
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_EXIST)

    def test_update_not_owner(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())
        post_id = data['id']
        self.login_test_user('new_login_name', '123456')
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'new_login_name',
                'title': 'New Title',
                'description': 'New description',
            }, self.token))
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_OWNER)