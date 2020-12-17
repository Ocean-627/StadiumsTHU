import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium


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
