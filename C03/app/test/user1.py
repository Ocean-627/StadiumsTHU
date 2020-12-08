import json

from django.test import TestCase
from app.models import *


class GetStadiumTest(TestCase):

    def setUp(self) -> None:
        User.objects.create(openId='cbx', loginToken=1)
        Stadium.objects.create(name='综合体育馆', information='综合体育馆', openTime='08:00', closeTime='18:00', openState=True,
                               foreDays=3)

    def test_get(self):
        params = {}
        resp = self.client.get('/api/user/stadium/', params, loginToken=1)
        content = json.loads(resp.content)
        print(content)
        self.assertEqual(resp.status_code, 200)
