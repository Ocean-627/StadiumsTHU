import json

from django.test import TestCase
from app.models import *


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
