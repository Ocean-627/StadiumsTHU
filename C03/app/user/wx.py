import requests
import json

appid = 'wx45b215f8db5d15f4'
secret = '33481c806778db936041d21679c0193b'
access_token = ''


def login(js_code):
    """
    登录并获取open_id
    """
    params = {
        'appid': appid,
        'secret': secret,
        'js_code': js_code,
        'grant_type': 'authorization_code'
    }
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    res = requests.get(url, params).json()
    return res


def get_access_token():
    """
    获取微信的access_token
    """
    params = {
        'appid': appid,
        'secret': secret,
        'grant_type': 'client_credential'
    }
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    res = requests.get(url, params).json()
    global access_token
    access_token = res.get('access_token')
    return res


def reserve_success_message(openId, type, date, content):
    """
    预订成功消息
    :param openId: 用户的openId
    :param type: 运动类型
    :param date: 时间
    :param content: 备注
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    template_id = 'hf9hHSc8OEHfmwicqL4rqLGaDwwJ5NRG4usDQwEJ7Mc'
    data = {
        'thing6': {
            'value': type
        },
        'time5': {
            'value': date
        },
        'thing9': {
            'value': content
        }
    }
    params = {
        'access_token': access_token,
        'touser': openId,
        'template_id': template_id,
        'data': data
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send' + '?access_token=' + params['access_token']
    res = requests.post(url, data=json.dumps(params), headers=headers).json()
    return res


def reserve_cancel_message(openId, type, date, content):
    """
    预订被取消消息
    :param openId: 用户的openId
    :param type: 运动类型
    :param date: 时间
    :param content: 备注
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    template_id = 'PdZ2sYAT_HXIkmho2wjfIbMS822H1f4d0xqiKFI6qgs'
    data = {
        'thing3': {
            'value': type
        },
        'time2': {
            'value': date
        },
        'thing6': {
            'value': content
        }
    }
    params = {
        'access_token': access_token,
        'touser': openId,
        'template_id': template_id,
        'data': data
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send' + '?access_token=' + params['access_token']
    res = requests.post(url, data=json.dumps(params), headers=headers).json()
    return res


def reserve_state_message(openId, type, date, content):
    """
    快开始或者快结束时发送
    :param openId: 用户的openId
    :param type: 运动类型
    :param date: 时间
    :param content: 备注
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    template_id = 'FLIjh95XJrOzgWWImzmXttYhs4eoCf9e6VAid0QjHbI'
    data = {
        'thing1': {
            'value': type
        },
        'time3': {
            'value': date
        },
        'thing6': {
            'value': content
        }
    }
    params = {
        'access_token': access_token,
        'touser': openId,
        'template_id': template_id,
        'data': data
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send' + '?access_token=' + params['access_token']
    res = requests.post(url, data=json.dumps(params), headers=headers).json()
    return res


if __name__ == '__main__':
    get_access_token()
    print(access_token)
    openId = 'ojXf94o4sj8EZKUS9l5mdn2NsH5U'
    res = reserve_state_message(openId, type='开军舰', date='2020-12-25', content='快开始啦')
    print(res)
