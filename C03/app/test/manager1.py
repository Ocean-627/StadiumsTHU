import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium


class TestManager(TestCase):
    def setUp(self) -> None:
        pass

    def test_manager(self):
        params = {
            'username': 'cbx',
            'password': 'UsingName123',
            'email': 'cbx@cnm.com',
            'userId': 7
        }
        resp = self.client.post('/api/manager/logon/', params)
        self.assertEqual(resp.status_code, 201)

        manager = Manager.objects.first()
        self.assertEqual(manager.password, params['password'])
        self.assertEqual(manager.userId, params['userId'])

        manager = Manager.objects.first()
        manager.loginToken = '1'

        # TODO: 设置cookies

        params = {}
        resp = self.client.get('/api/manager/manager/', params)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content[0]['username'], 'cbx')

        params = {
            'username': 'haha',
            'loginToken': '3',
            'userId': 9
        }
        resp = self.client.post('/api/manager/manager/', params)
        self.assertEqual(resp.status_code, 200)
        manager = Manager.objects.first()
        self.assertEqual(manager.userId, 7)
        self.assertEqual(manager.loginToken, '1')
        self.assertEqual(manager.username, params['username'])




