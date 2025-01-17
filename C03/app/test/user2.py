import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium

"""
测试时间 2020-11-24
原因：测试用户的各项基本动态操作，如预订，评论，收藏
结果: 正常
第一次修改 2020-12-18
原因：变更了预订已经评论的方式
结果：发现一处修改model没有保存的bug，一处逻辑bug
"""


class TestReserve(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_reserve(self):
        params = {
            'duration_id': 160
        }
        resp = self.client.post('/api/user/reserve/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)
        duration = Duration.objects.filter(id=160).first()
        self.assertEqual(duration.accessible, False)
        self.assertEqual(duration.user.userId, 123)

        resp = self.client.post('/api/user/reserve/', params, **self.headers)
        content = json.loads(resp.content)
        self.assertIn('error', content)
        self.assertEqual(resp.status_code, 400)

        params = {
            'id': 1,
            'cancel': 1
        }
        resp = self.client.put('/api/user/reserve/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        duration = Duration.objects.filter(id=160).first()
        self.assertEqual(duration.accessible, True)

        Stadium.objects.all().delete()
        self.assertEqual(len(ReserveEvent.objects.all()), 1)

        params = {
            'id': 1
        }
        resp = self.client.delete('/api/user/reserve/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(ReserveEvent.objects.all()), 0)


class TestComment(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_comment(self):
        params = {
            'duration_id': 1
        }
        resp = self.client.post('/api/user/reserve/', params, **self.headers)
        reserve = ReserveEvent.objects.first()
        self.assertEqual(reserve.has_comments, False)

        params = {
            'reserve_id': 1,
            'content': 'nice',
            'score': 4
        }
        resp = self.client.post('/api/user/comment/', params, **self.headers)
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertIn('error', content)

        params['content'] = '我会告诉你我是在用十五字来混评论吗'
        resp = self.client.post('/api/user/comment/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        params['score'] = 5
        params['content'] = 'usingnamespacestd'
        resp = self.client.post('/api/user/comment/', params, **self.headers)

        resp = self.client.get('/api/user/stadium/', {}, **self.headers)
        content = json.loads(resp.content)
        stadium = content[0]
        self.assertEqual(stadium['score'], 4.5)
        self.assertEqual(stadium['comments'], 2)

        params = {
            'comment_id': 2,
        }
        resp = self.client.delete('/api/user/comment/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(Comment.objects.all()), 1)

        resp = self.client.get('/api/user/stadium/', {}, **self.headers)
        content = json.loads(resp.content)
        stadium = content[0]
        self.assertEqual(stadium['score'], 4)
        self.assertEqual(stadium['comments'], 1)

        params = {
            'comment_id': 1
        }
        resp = self.client.delete('/api/user/comment/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(Comment.objects.all()), 0)
        reserve = ReserveEvent.objects.first()
        self.assertEqual(reserve.has_comments, False)


class TestCollect(TestCase):
    def setUp(self) -> None:
        User.objects.create(userId=123, loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_collect(self):
        params = {
            'stadium_id': 1,
        }
        resp = self.client.post('/api/user/collect/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(len(CollectEvent.objects.all()), 1)

        resp = self.client.post('/api/user/collect/', params, **self.headers)
        self.assertEqual(resp.status_code, 400)

        resp = self.client.get('/api/user/stadium/', {}, **self.headers)
        content = json.loads(resp.content)
        stadium = content[0]
        self.assertEqual(stadium['collect'], 1)

        params = {
            'collect_id': 1,
        }
        resp = self.client.delete('/api/user/collect/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/api/user/stadium/', {}, **self.headers)
        content = json.loads(resp.content)
        stadium = content[0]
        self.assertEqual(stadium['collect'], None)
