import json

from django.test import TestCase
from app.models import *

"""
测试时间 2020-12-1
原因：增加了站内会话功能
结果: 发现了数据表中auto_now和auto_now_add导致的bug

第一次修改 2020-12-3
原因：需要对会话进行排序，筛选等
结果：正常
"""


class TestSession(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        self.headers = {'HTTP_loginToken': 1}

    def test_session(self):
        params = {}
        resp = self.client.post('/api/user/session/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)
        session = Session.objects.get(id=1)
        self.assertEqual(session.user_id, 1)

        resp = self.client.post('/api/user/session/', params, **self.headers)
        resp = self.client.get('/api/user/session/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 2)

        params = {
            'sort': '-createTime'
        }
        resp = self.client.get('/api/user/session/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(content[0]['id'], 2)
        self.assertEqual(content[1]['id'], 1)


class TestMessage(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        Session.objects.create(user_id=1)
        self.headers = {'HTTP_loginToken': 1}

    def test_message(self):
        Session.objects.create(user_id=1)
        params = {
            'session_id': 1,
            'content': 'nice'
        }
        resp = self.client.post('/api/user/message/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        resp = self.client.get('/api/user/message/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(content[0]['sender'], 'U')
        self.assertEqual(content[0]['content'], 'nice')

        params = {
            'sort': '-updateTime'
        }
        resp = self.client.get('/api/user/session/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(content[0]['id'], 1)
        self.assertEqual(content[1]['id'], 2)
