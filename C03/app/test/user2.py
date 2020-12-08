import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium


class TestReserve(TestCase):
    def setUp(self) -> None:
        User.objects.create(openId='cbx', loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_reserve(self):
        params = {
            'duration_id': 160
        }
        resp = self.client.post('/api/user/reserve/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        duration = Duration.objects.filter(id=160).first()
        self.assertEqual(duration.accessible, False)
        self.assertEqual(duration.user.openId, 'cbx')

        resp = self.client.post('/api/user/reserve/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertIn('error', content)
        self.assertEqual(resp.status_code, 400)

        params = {
            'event_id': 1
        }
        resp = self.client.put('/api/user/reserve/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        duration = Duration.objects.filter(id=160).first()
        self.assertEqual(duration.accessible, True)

