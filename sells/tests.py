# coding:utf-8
import json
import hashlib
from django.test import TestCase
from django.test.client import Client
from django.utils.http import urlquote
from wrappers.wrapper import get_dict_md5
from errnos import errno


class AuthTestCase(TestCase):

    def add_token(self, data, token):
        data['token'] = get_dict_md5(data, token)
        return data

    def login_test_user(self, username, password):
        response = self.client.post('/account/user/', {'username': username,
                                                       'password': hashlib.md5(password).hexdigest()})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('user_id' in data.keys())
        self.user_id = str(data['user_id'])
        self.token = hashlib.md5(password).hexdigest()


class NewSellPostTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_new_sell_post_normal(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        response = self.client.get('/sell/post/' + str(post_id) + '/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEquals(data['post']['title'], 'Sell Title')
        self.assertEquals(data['post']['description'], 'New Sell!')
        self.assertTrue('post_id' in data['post'].keys())
        self.assertTrue('user_id' in data['post'].keys())
        self.assertTrue('image_set_id' in data['post'].keys())
        self.assertTrue('post_date' in data['post'].keys())
        self.assertTrue('modify_date' in data['post'].keys())

    def test_new_sell_post_utf_8(self):
        self.login_test_user('login_name', '123456')
        title = u'出售 test 信息'
        description = u'出售 test 信息描述'
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': urlquote(title),
                'description': urlquote(description),
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        response = self.client.get('/sell/post/' + str(post_id) + '/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEquals(data['post']['title'], title)
        self.assertEquals(data['post']['description'], description)
        self.assertTrue('post_id' in data['post'].keys())
        self.assertTrue('user_id' in data['post'].keys())
        self.assertTrue('image_set_id' in data['post'].keys())
        self.assertTrue('post_date' in data['post'].keys())
        self.assertTrue('modify_date' in data['post'].keys())

    def test_empty_allowed_field(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())

    def test_no_user_name(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token({}, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISSING_PARAMETER)


class UpdateSellPostTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_update_post_normal(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'New Title',
                'description': 'New description',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.get('/sell/post/' + str(post_id) + '/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEquals(data['post']['title'], 'New Title')
        self.assertEquals(data['post']['description'], 'New description')

    def test_update_allow_empty(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'user_id': self.user_id,
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_update_not_exist(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id'] + 100
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'user_id': self.user_id,
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
                'user_id': self.user_id,
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        self.login_test_user('new_login_name', '123456')
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'New Title',
                'description': 'New description',
            }, self.token))
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_OWNER)


class DeleteSellPostTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_delete_post_normal(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'user_id': self.user_id
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        response = self.client.get('/sell/post/' + str(post_id) + '/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_EXIST)

    def test_delete_not_exist(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id'] + 100
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'user_id': self.user_id
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_EXIST)

    def test_delete_not_owner(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': 'Sell Title',
                'description': 'New Sell!',
                'images': '1,2,3',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        self.login_test_user('new_login_name', '123456')
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'user_id': self.user_id
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_OWNER)

    def test_delete_no_username(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token({
            'user_id': self.user_id,
        }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        post_id = data['post_id']
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token({}, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISSING_PARAMETER)


class GetSellPostsTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        self.login_test_user('login_name', '123456')
        for i in range(100):
            self.create_post('title_' + str(i))

    def create_post(self, title):
        response = self.client.post('/sell/post/', self.add_token(
            {
                'user_id': self.user_id,
                'title': title,
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('post_id' in data.keys())
        return data['post_id']

    def test_get_posts_normal(self):
        response = self.client.get('/sell/posts/1/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('posts' in data.keys())
        self.assertTrue(data['posts'][0]['title'], 'title_99')
        self.assertTrue(data['posts'][1]['title'], 'title_98')

    def test_get_posts_zero_page_num(self):
        response = self.client.get('/sell/posts/0/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('posts' in data.keys())
        self.assertTrue(data['posts'][0]['title'], 'title_99')
        self.assertTrue(data['posts'][1]['title'], 'title_98')