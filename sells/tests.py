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

    def logout_test_user(self):
        response = self.client.delete('/account/token/', self.add_token(
            {
                'username': 'login_name'
            }, self.token))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])


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
        post_id = data['id']
        response = self.client.get('/sell/post/' + str(post_id) + '/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEquals(data['post']['title'], 'Sell Title')
        self.assertEquals(data['post']['description'], 'New Sell!')
        self.assertTrue('user' in data['post'].keys())
        self.assertTrue('image_set' in data['post'].keys())
        self.assertTrue('post_date' in data['post'].keys())
        self.assertTrue('modify_date' in data['post'].keys())

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

    def test_no_user_name(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token({}, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISSING_PARAMETER)

    def test_not_login(self):
        self.login_test_user('login_name', '123456')
        self.logout_test_user()
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NO_TOKEN)


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

    def test_update_not_login(self):
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
        self.logout_test_user()
        response = self.client.put('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'login_name',
                'title': 'New Title',
                'description': 'New description',
            }, self.token))
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NO_TOKEN)


class DeleteSellPostTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()

    def test_delete_post_normal(self):
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
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'login_name'
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
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'login_name'
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_EXIST)

    def test_delete_not_owner(self):
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
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token(
            {
                'username': 'new_login_name'
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NOT_OWNER)

    def test_delete_no_username(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token({
            'username': 'login_name',
        }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())
        post_id = data['id']
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token({}, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_MISSING_PARAMETER)

    def test_delete_not_login(self):
        self.login_test_user('login_name', '123456')
        response = self.client.post('/sell/post/', self.add_token({
            'username': 'login_name',
        }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())
        post_id = data['id']
        self.logout_test_user()
        response = self.client.delete('/sell/post/' + str(post_id) + '/', self.add_token({
            'username': 'login_name',
        }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['errno'], errno.ERRNO_NO_TOKEN)


class GetSellPostsTestCase(AuthTestCase):

    def setUp(self):
        self.client = Client()
        self.login_test_user('login_name', '123456')
        for i in range(100):
            self.create_post('title_' + str(i))
        self.logout_test_user()

    def create_post(self, title):
        response = self.client.post('/sell/post/', self.add_token(
            {
                'username': 'login_name',
                'title': title,
            }, self.token))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue('id' in data.keys())
        return data['id']

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