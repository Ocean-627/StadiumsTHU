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
            'userId': '7'
        }
        resp = self.client.post('/api/manager/logon/', params)
        self.assertEqual(resp.status_code, 201)
