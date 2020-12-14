import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium


class TestChangeSchedule(TestCase):
    def setUp(self) -> None:
        Manager.objects.create(username='cbx', password='123', userId=1, email='cbx@qq.com', loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_schedule(self):
        params = {
            'stadium_id': 1,
            'openState': 1,
            'openTime': '07:00',
            'closeTime': '19:00',
            'startDate': '2020-12-25',
            'foreDays': 3
        }
        resp = self.client.post('/api/manager/changeschedule/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        schedule = ChangeSchedule.objects.first()
        self.assertEqual(schedule.manager.id, 1)
        self.assertEqual(schedule.stadium.id, 1)
        self.assertEqual(schedule.foreDays, 3)
        self.assertEqual(schedule.startDate, params['startDate'])
