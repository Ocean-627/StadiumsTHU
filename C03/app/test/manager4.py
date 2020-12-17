import json

from django.test import TestCase
from app.models import *

"""
测试时间 2020-12-17
原因：测试管理员端对站内会话的处理，以及和用户的交互
结果: 发现了获取用户图片时的bug
"""


class TestSession(TestCase):
    def setUp(self) -> None:
        Manager.objects.create(username='cbx', password='123', userId=1, email='cbx@qq.com', loginToken=1)
        self.manager_headers = {'HTTP_loginToken': 1}

        User.objects.create(userId=2018011891, loginToken=2)
        User.objects.create(userId=2018011894, loginToken=3)
        self.user1_headers = {'HTTP_loginToken': 2}
        self.user2_headers = {'HTTP_loginToken': 3}

    def test_chat(self):
        params = {
            'user_id': 1
        }
        resp = self.client.post('/api/manager/session/', params, **self.manager_headers)
        self.assertEqual(resp.status_code, 201)

        params = {
            'session_id': 1,
            'content': '1'
        }
        resp = self.client.post('/api/manager/message/', params, **self.manager_headers)
        self.assertEqual(resp.status_code, 201)

        params = {}
        resp = self.client.get('/api/user/message/', params, **self.user1_headers)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content[0]['sender'], 'M')

        params = {
            'session_id': 1,
        }
        resp = self.client.get('/api/user/message/', params, **self.user1_headers)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 1)

        params = {
            'id': 1,
            'checked': 1
        }
        # 用户的session是没有分页的，因此不需要再取results
        resp = self.client.get('/api/user/session/', params, **self.user1_headers)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 1)

        params = {}
        resp = self.client.get('/api/user/session/', params, **self.user2_headers)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 0)

        params = {
            'session_id': 1,
            'content': 2
        }
        resp = self.client.post('/api/user/message/', params, **self.user1_headers)

        params = {}
        resp = self.client.get('/api/manager/session/', params, **self.manager_headers)
        self.assertEqual(resp.status_code, 200)

        content = json.loads(resp.content)['results']
        self.assertEqual(content[0]['checked'], False)

        params = {
            'session_id': 1,
            'open': False
        }
        resp = self.client.put('/api/manager/session/', params, **self.manager_headers, content_type='application/json')
        session = Session.objects.first()
        self.assertEqual(session.open, False)
