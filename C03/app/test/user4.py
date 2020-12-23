import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium

"""
测试时间 2020-12-18
原因：改用功能较少的站内信息模块
结果：正常

第一次修改 2020-12-23
原因：增加了预订连续场馆
结果：正常

第二次修改 2020-12-23
原因：修改了计算price的bug
结果：正常
"""


class TestNews(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_news(self):
        params = {
            'duration_id': 1
        }
        resp = self.client.post('/api/user/reserve/', params, **self.headers)
        self.assertEqual(len(News.objects.all()), 1)
        news = News.objects.first()
        self.assertEqual(news.user_id, 1)

        params = {}
        resp = self.client.put('/api/user/reserve/', params, **self.headers, content_type='application/json')
        self.assertEqual(len(News.objects.all()), 1)

        params = {
            'cancel': 1,
            'id': 1
        }
        resp = self.client.put('/api/user/reserve/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        params = {}
        resp = self.client.get('/api/user/news/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(content['count'], 2)
        self.assertEqual(content['results'][0]['id'], 2)


class TestBatchReserve(TestCase):

    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_batchreserve(self):
        params = {
            'duration_id': 1,
            'startTime': '10:00',
            'endTime': '12:00'
        }
        resp = self.client.post('/api/user/batchreserve/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        reserve = ReserveEvent.objects.first()
        self.assertEqual(reserve.price, 60)

        user = User.objects.first()

        duration = Duration.objects.get(id=1)
        self.assertEqual(duration.accessible, 0)
        self.assertEqual(duration.user, user)

        duration = Duration.objects.get(id=3)
        self.assertEqual(duration.accessible, 0)
        self.assertEqual(duration.user, user)

        params = {
            'duration_id': 3,
            'startTime': '11:00',
            'endTime': '13:00'
        }
        resp = self.client.post('/api/user/batchreserve/', params, **self.headers)
        self.assertEqual(resp.status_code, 400)

        params = {
            'duration_id': 5,
            'startTime': '12:00',
            'endTime': '14:00'
        }
        resp = self.client.post('/api/user/batchreserve/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        params = {
            'id': 1,
            'cancel': 1
        }
        resp = self.client.put('/api/user/reserve/', params, **self.headers, content_type='application/json')
        duration = Duration.objects.get(id=1)
        self.assertEqual(duration.accessible, 1)

        duration = Duration.objects.get(id=3)
        self.assertEqual(duration.accessible, 1)
