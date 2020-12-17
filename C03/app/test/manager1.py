import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium

"""
测试时间 2020-11-19
原因：测试管理员对于静态资源的访问
结果: 正常

第一次修改 2020-11-25
原因：增加了对用户进行筛选
结果：发现了部分表项不能排序的bug

第二次修改 2020-11-27
原因：增加了分页功能
结果：正常
"""


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
        manager.save()

        params = {}
        headers = {'HTTP_loginToken': '1'}
        resp = self.client.get('/api/manager/manager/', params, **headers)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['username'], 'cbx')

        params = {
            'username': 'haha',
            'loginToken': '3',
            'userId': 9
        }
        resp = self.client.post('/api/manager/manager/', params, **headers)
        self.assertEqual(resp.status_code, 200)
        manager = Manager.objects.first()
        self.assertEqual(manager.userId, 7)
        self.assertEqual(manager.loginToken, '1')
        self.assertEqual(manager.username, params['username'])


class TestStadium(TestCase):
    def setUp(self) -> None:
        Stadium.objects.create(name='综合体育馆', information='综合体育馆', openTime='08:00', closeTime='18:00', openState=True,
                               foreDays=3)
        Stadium.objects.create(name='陈明游泳馆', information='陈明游泳馆', openTime='09:00', closeTime='19:00', openState=True,
                               foreDays=2)

    def test_stadium(self):
        params = {}
        resp = self.client.get('/api/manager/stadium/', params)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['name'], '综合体育馆')

        params = {
            'stadium_id': 1,
            'name': '紫荆气膜馆',
            'information': 'haha',
            'openTime': '10:00'
        }
        resp = self.client.post('/api/manager/stadium/', params)
        stadium = Stadium.objects.get(id=1)
        self.assertEqual(stadium.name, params['name'])
        self.assertEqual(stadium.information, params['information'])
        self.assertEqual(stadium.openTime, "08:00")


class TestUser(TestCase):
    def setUp(self) -> None:
        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        chars.reverse()
        for i in range(10):
            User.objects.create(userId=i, nickName=chars[i] * 5)

    def test_user(self):
        params = {}
        resp = self.client.get('/api/manager/user/', params)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)['results']
        self.assertEqual(len(content), 10)
        self.assertEqual(content[0]['userId'], 0)

        params = {
            'page': 2,
            'size': 6
        }
        resp = self.client.get('/api/manager/user/', params)
        content = json.loads(resp.content)['results']
        self.assertEqual(len(content), 4)
        self.assertEqual(content[0]['userId'], 6)

        params = {
            'page': 2,
            'size': 3,
            'sort': '-nickName'
        }
        resp = self.client.get('/api/manager/user/', params)
        content = json.loads(resp.content)['results']
        self.assertEqual(content[0]['nickName'], 'g' * 5)
        self.assertEqual(content[1]['nickName'], 'f' * 5)
        self.assertEqual(content[2]['nickName'], 'e' * 5)
