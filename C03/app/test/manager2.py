import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium

"""
测试时间 2020-12-04
原因：测试管理员对各种静态资源的访问
结果: 发现了管理员所需信息返回不全的bug

第一次修改 2020-12-17
原因：增加了创建场馆功能
结果：正常
"""


class TestStaticSource(TestCase):
    def setUp(self) -> None:
        initStadium(stadiums[0])
        initStadium(stadiums[1])

    def test_static(self):
        params = {}
        resp = self.client.get('/api/manager/court/', params)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 20)

        params = {
            'stadium_id': 1,
            'type': '羽毛球'
        }
        resp = self.client.get('/api/manager/court/', params)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 5)

        params = {
            'court_id': 1
        }
        resp = self.client.get('/api/manager/duration/', params)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 8)


class TestCreateStadium(TestCase):
    def setUp(self) -> None:
        Manager.objects.create(username='cbx', password='123', userId=1, email='cbx@qq.com', loginToken=1)
        self.headers = {'HTTP_loginToken': 1}

    def test_create(self):
        params = {
            'name': '测试场馆',
            'information': '测试用',
            'openTime': '08:00',
            'closeTime': '10:00',
            'openState': 1,
            'foreDays': 3,
            'createTime': '2020-12-25'
        }
        resp = self.client.post('/api/manager/stadium/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        stadium = Stadium.objects.first()
        self.assertEqual(stadium.openState, 0)
        self.assertEqual(stadium.createTime, params['createTime'])

        params = {
            'stadium_id': 1,
            'type': '羽毛球',
            'openingHours': '08:00-12:00,13:00-17:00',
            'openState': 1
        }
        resp = self.client.post('/api/manager/courttype/', params, **self.headers)
        self.assertEqual(resp.status_code, 400)

        params['num'] = 4
        resp = self.client.post('/api/manager/courttype/', params, **self.headers)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(Court.objects.all()), 4)


class TestReserve(TestCase):
    def setUp(self) -> None:
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        User.objects.create(userId=2018011891, loginToken=1)
        User.objects.create(userId=2018011904, loginToken=3)
        self.user1_headers = {'HTTP_loginToken': 1}
        self.user2_headers = {'HTTP_loginToken': 3}

    def test_reserve(self):
        params = {
            'duration_id': 1
        }
        resp = self.client.post('/api/user/reserve/', params, **self.user1_headers)
        self.assertEqual(resp.status_code, 201)

        params = {
            'duration_id': 2
        }
        resp = self.client.post('/api/user/reserve/', params, **self.user1_headers)
        self.assertEqual(resp.status_code, 201)

        params = {
            'duration_id': 10
        }
        resp = self.client.post('/api/user/reserve/', params, **self.user2_headers)
        self.assertEqual(resp.status_code, 201)

        params = {
            'user_id': 1
        }
        resp = self.client.get('/api/manager/reserveevent/', params)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 2)

        params = {
            'stadium_id': 1
        }
        resp = self.client.get('/api/manager/reserveevent/', params)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 3)
