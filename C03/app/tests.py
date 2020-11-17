from django.test import TestCase
from app.models import *
import json


# Create your tests here.
class TestTest(TestCase):
    """
    测试如何使用测试
    """

    def test(self):
        rsp = self.client.post('/test/')
        content = json.loads(rsp.content)
        self.assertEqual(content['test'], 'just for test')


class LogonTest(TestCase):
    """
    测试注册
    """

    def test_logon(self):
        # 错误参数
        params = {
            'username': 'cbx',
            'password': 'UsingNamespaceStd',
            'userId': 2018011891,
            'email': 'cbx@qq.com'
        }
        rsp = self.client.post('/api/user/logon/', params)
        content = json.loads(rsp.content)
        self.assertEqual(rsp.status_code, 200)
        self.assertIn('error', content)
        # 正确参数
        params['password'] = 'Using123456'
        rsp = self.client.post('/api/user/logon/', params)
        content = json.loads(rsp.content)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(content['message'], 'ok')
        # 使用重复学生编号
        rsp = self.client.post('/api/user/logon/', params)
        content = json.loads(rsp.content)
        self.assertEqual(rsp.status_code, 200)
        self.assertIn('error', content)


class LoginTest(TestCase):
    """
    测试登录
    """

    def setUp(self):
        User.objects.create(username='cbx', password='UsingNamespaceStd12', userId=2018011891, email='cbx@qq.com')

    def test_Login(self):
        # 密码错误
        params = {
            'userId': 2018011891,
            'password': 'UsingNamespaceStd1',
        }
        rsp = self.client.post('/api/user/login/', params)
        content = json.loads(rsp.content)
        self.assertEqual(rsp.status_code, 200)
        self.assertIn('error', content)
        # 密码正确
        params['password'] = 'UsingNamespaceStd12'
        rsp = self.client.post('/api/user/login/', params)
        content = json.loads(rsp.content)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(content['message'], 'ok')


class GetStadiumTest(TestCase):
    """
    测试查看场馆信息
    """

    def setUp(self):
        User.objects.create(username='cbx', password='UsingNamespaceStd12', userId=2018011891, email='cbx@qq.com')
        Stadium.objects.create(name='cbx的场馆', information='专门用来测试', openingHours='08:00-12:00, 13:00-17:00',
                               openTime="08:00", closeTime="17:00", openState=True, foreDays=3, durations='01:00')
        Stadium.objects.create(name='xxh的场馆', information='第二个测试的场馆', openingHours='08:00-12:00, 13:00-17:00',
                               openTime="08:00", closeTime="17:00", openState=True, foreDays=3, durations='01:00')
        params = {
            'userId': 2018011891,
            'password': 'UsingNamespaceStd12'
        }
        rsp = self.client.post('/api/user/login/', params)
        content = json.loads(rsp.content)
        self.loginToken = content['loginToken']

    def test_get_stadium(self):
        params = {}
        rsp = self.client.get('/api/user/stadium/', params)
        self.assertEqual(rsp.status_code, 403)
        content = json.loads(rsp.content)
        self.assertEqual(content['error'], 'Requires loginToken')
        params = {
            'loginToken': self.loginToken
        }
        rsp = self.client.get('/api/user/stadium/', params)
        self.assertEqual(rsp.status_code, 200)
        content = json.loads(rsp.content)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['name'], 'cbx的场馆')
        self.assertEqual(content[1]['name'], 'xxh的场馆')
        self.assertEqual(content[0]['information'], '专门用来测试')
        self.assertEqual(content[1]['information'], '第二个测试的场馆')


class ReverseDurationTest(TestCase):
    """
    测试预订场馆
    """

    def setUp(self):
        User.objects.create(username='cbx', password='UsingNamespaceStd12', userId=2018011891, email='cbx@qq.com')
        Stadium.objects.create(name='cbx的场馆', information='专门用来测试', openingHours='08:00-12:00, 13:00-17:00',
                               openTime="08:00", closeTime="17:00", openState=True, foreDays=3, durations='01:00')
        Court.objects.create(stadium_id=1, type='羽毛球', price=30, openState=True, floor=1, location='306A')
        Duration.objects.create(stadium_id=1, court_id=1, date='11.16', startTime='08:00', endTime='09:00',
                                openState=True, accessible=True)
        params = {
            'userId': 2018011891,
            'password': 'UsingNamespaceStd12'
        }
        rsp = self.client.post('/api/user/login/', params)
        content = json.loads(rsp.content)
        self.loginToken = content['loginToken']

    def test_reserve(self):
        params = {
            'durationId': 1
        }
        rsp = self.client.post('/api/user/reserve/' + "?loginToken=" + self.loginToken, params)
        content = json.loads(rsp.content)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(content['message'], 'ok')
        # 查看数据库是否正确被更改
        duration = Duration.objects.all()[0]
        self.assertFalse(duration.accessible)
        self.assertEqual(duration.user_id, 1)
        event = ReserveEvent.objects.all()[0]
        self.assertEqual(event.user_id, 1)
        self.assertEqual(event.duration_id, 1)
        # 取消操作

