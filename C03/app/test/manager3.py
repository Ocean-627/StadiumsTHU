import json

from django.test import TestCase
from app.models import *
from app.utils.utils import stadiums
from app.utils.utils import initStadium

"""
测试时间 2020-12-17
原因：确定了几种管理员的事件，测试接口是否正常
结果: 发现了一些拼写错误导致的bug
      发现了场地占用事件无法正确更改预约
      
第一次修改 2020-12-17
原因：测试加入黑名单功能
结果：正常

第二次修改 2020-12-18
原因：加入了对ChangeDuration和AddEvent的撤销功能
结果：正常

第三次修改 2020-12-19
原因：增加了user的openId,预留场馆时应该发送消息
"""


class TestDefault(TestCase):
    def setUp(self) -> None:
        Manager.objects.create(username='cbx', password='123', userId=1, email='cbx@qq.com', loginToken=1)
        self.headers = {'HTTP_loginToken': 1}
        User.objects.create(userId=2018011891, inBlacklist=1, defaults=4, name='战神')
        for _ in range(4):
            Default.objects.create(user_id=1)

    def test_default(self):
        self.assertEqual(len(Default.objects.all()), 4)
        params = {
            'default_id': 1
        }
        resp = self.client.put('/api/manager/default/', params, **self.headers, content_type='application/json')

        operation = OtherOperation.objects.first()
        self.assertEqual(operation.type, '撤销信用记录')
        self.assertEqual(resp.status_code, 200)
        user = User.objects.first()
        self.assertEqual(user.defaults, 3)
        self.assertEqual(user.inBlacklist, 1)

        params = {
            'default_id': 2
        }
        resp = self.client.put('/api/manager/default/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        user = User.objects.first()
        self.assertEqual(user.defaults, 2)
        self.assertEqual(user.inBlacklist, 0)

        resp = self.client.get('/api/manager/default/', params, **self.headers)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)['results']
        self.assertEqual(len(content), 4)
        self.assertEqual(content[0]['cancel'], 1)
        self.assertEqual(content[1]['cancel'], 1)


class TestChangeDuration(TestCase):
    def setUp(self) -> None:
        Manager.objects.create(username='cbx', password='123', userId=1, email='cbx@qq.com', loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

    def test_changeduration(self):
        params = {
            'courtType_id': 1,
            'openingHours': '08:00-12:00,13:00-17:00',
            'date': '2020-12-25',
            'price': 30,
            'openState': 1,
        }
        resp = self.client.post('/api/manager/changeduration/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        params['courtType_id'] = 2
        resp = self.client.post('/api/manager/changeduration/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        params = {}
        resp = self.client.get('/api/manager/changeduration/', params, **self.headers)
        content = json.loads(resp.content)

        self.assertEqual(content[0]['price'], 30)
        self.assertEqual(content[1]['openState'], 1)

        params = {
            'id': 1
        }
        resp = self.client.put('/api/manager/changeduration/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        changeDuration = ChangeDuration.objects.first()
        self.assertEqual(changeDuration.state, 1)

        resp = self.client.put('/api/manager/changeduration/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 400)


class TestAddEvent(TestCase):
    def setUp(self) -> None:
        Manager.objects.create(username='cbx', password='123', userId=1, email='cbx@qq.com', loginToken=1)
        initStadium(stadiums[0])
        initStadium(stadiums[1])
        self.headers = {'HTTP_loginToken': 1}

        User.objects.create(userId=2018011891, loginToken=1, openId='123')
        self.user_headers = {'HTTP_loginToken': 1}

    def test_addevent(self):
        params = {
            'duration_id': 1
        }
        resp = self.client.post('/api/user/reserve/', params, **self.user_headers)
        self.assertEqual(resp.status_code, 201)

        params = {
            'duration_id': 3
        }
        resp = self.client.post('/api/user/reserve/', params, **self.user_headers)
        self.assertEqual(resp.status_code, 201)

        params = {
            'duration_id': 7
        }
        resp = self.client.post('/api/user/reserve/', params, **self.user_headers)
        self.assertEqual(resp.status_code, 201)

        self.assertEqual(len(News.objects.all()), 3)

        params = {
            'court_id': 1,
            'startTime': '10:00',
            'endTime': '13:00',
            'date': '2020-12-30',
        }
        resp = self.client.post('/api/manager/addevent/', params, **self.headers)
        self.assertEqual(resp.status_code, 200)

        duration = Duration.objects.get(id=1)
        self.assertEqual(duration.openState, 0)
        duration = Duration.objects.get(id=3)
        self.assertEqual(duration.openState, 0)
        duration = Duration.objects.get(id=5)
        self.assertEqual(duration.openState, 0)

        self.assertEqual(ReserveEvent.objects.get(id=1).cancel, 1)
        self.assertEqual(ReserveEvent.objects.get(id=2).cancel, 1)
        self.assertEqual(ReserveEvent.objects.get(id=3).cancel, 0)

        self.assertEqual(len(News.objects.all()), 5)

        addEvent = AddEvent.objects.first()
        self.assertEqual(addEvent.state, 2)
        params = {
            'id': 1
        }
        resp = self.client.put('/api/manager/addevent/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

        params = {
            'court_id': 1,
            'startTime': '10:00',
            'endTime': '13:00',
            'date': '2020-12-31',
        }
        resp = self.client.post('/api/manager/addevent/', params, **self.headers)
        self.assertEqual(resp.status_code, 200)
        params = {
            'id': 2
        }
        resp = self.client.put('/api/manager/addevent/', params, **self.headers, content_type='application/json')
        addEvent = AddEvent.objects.get(id=2)
        self.assertEqual(addEvent.state, 1)


class TestAddBlacklist(TestCase):
    def setUp(self) -> None:
        Manager.objects.create(username='cbx', password='123', userId=1, email='cbx@qq.com', loginToken=1)
        self.headers = {'HTTP_loginToken': 1}
        User.objects.create(userId=2018011891, name='战神')

    def test_addblacklist(self):
        params = {
            'user_id': 1,
        }
        resp = self.client.post('/api/manager/blacklist/', params, **self.headers)
        self.assertEqual(resp.status_code, 201)

        operation = OtherOperation.objects.first()
        self.assertEqual(operation.type, '移入黑名单')

        user = User.objects.first()
        self.assertEqual(user.inBlacklist, 1)

        params = {
            'user_id': 1
        }
        resp = self.client.put('/api/manager/blacklist/', params, **self.headers, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        operation = OtherOperation.objects.last()
        self.assertEqual(operation.type, '移除黑名单')

        user = User.objects.first()
        self.assertEqual(user.inBlacklist, 0)
