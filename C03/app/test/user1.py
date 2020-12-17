import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium


class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        self.headers = {'HTTP_loginToken': 1}

    def test_user(self):
        params = {
            'userId': 456,
            'phone': '18801225328',
            'nickName': '三个字'
        }
        resp = self.client.post('/api/user/user/', params, **self.headers)
        user = User.objects.all().first()
        self.assertEqual(user.nickName, params['nickName'])
        self.assertEqual(user.phone, params['phone'])
        self.assertEqual(user.userId, 123)


class GetStadiumTest(TestCase):

    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        Stadium.objects.create(name='综合体育馆', information='综合体育馆', openTime='08:00', closeTime='18:00', openState=True,
                               foreDays=3)
        Stadium.objects.create(name='陈明游泳馆', information='陈明游泳馆', openTime='09:00', closeTime='19:00', openState=True,
                               foreDays=2)
        self.headers = {'HTTP_loginToken': 1}

    def test_get(self):
        params = {}

        resp = self.client.get('/api/user/stadium/', params)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get('/api/user/stadium/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['name'], '综合体育馆')
        self.assertEqual(content[1]['name'], '陈明游泳馆')
        self.assertEqual(content[0]['score'], 3)

        params = {
            'info': '综合'
        }
        resp = self.client.get('/api/user/stadium/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['name'], '综合体育馆')

        params = {
            'foreGt': 2
        }
        resp = self.client.get('/api/user/stadium/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['name'], '综合体育馆')


class GetCourtTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_get(self):
        self.assertEqual(len(Stadium.objects.all()), 2)
        self.assertEqual(len(CourtType.objects.all()), 4)
        self.assertEqual(len(Court.objects.all()), 20)

        params = {
            'type': '羽毛球',
            'stadium_id': 1
        }
        resp = self.client.get('/api/user/court/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 5)
        self.assertEqual(content[0]['stadium'], 1)
        self.assertEqual(content[0]['type'], '羽毛球')

        params = {
            'location': '304B'
        }
        resp = self.client.get('/api/user/court/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 10)


class GetDurationTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=456, loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_get(self):
        self.assertEqual(len(Duration.objects.all()), 160)
        params = {
            'court_id': 1,
            'startTime': '12:00'
        }
        resp = self.client.get('/api/user/duration/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(len(content), 1)


class TestRelationship(TestCase):
    def setUp(self) -> None:
        initStadium(stadiums[0])
        initStadium(stadiums[1])

    def test_delete(self):
        stadium = Stadium.objects.first()
        stadium.delete()
        self.assertEqual(len(CourtType.objects.all()), 2)
        self.assertEqual(len(Court.objects.all()), 10)
        self.assertEqual(len(Duration.objects.all()), 80)
