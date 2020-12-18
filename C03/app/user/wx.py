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


def reserve_success_message(openId, data):
    """
    :param openId: 用户的openId
    :param data: 要发送的内容
    """
    headers = {
        'Content-Type': 'application/json'
    }
    template_id = 'hf9hHSc8OEHfmwicqL4rqLGaDwwJ5NRG4usDQwEJ7Mc'
    params = {
        'access_token': access_token,
        'touser': openId,
        'template_id': template_id,
        'data': data
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=ACCESS_TOKEN'
    res = requests.post(url, data=json.dumps(params), headers=headers).json()
    return res


def reserve_cancel_message(openId, data):
    """
        :param openId: 用户的openId
        :param data: 要发送的内容
        """
    headers = {
        'Content-Type': 'application/json'
    }
    template_id = 'PdZ2sYAT_HXIkmho2wjfIbMS822H1f4d0xqiKFI6qgs'
    params = {
        'access_token': access_token,
        'touser': openId,
        'template_id': template_id,
        'data': data
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=ACCESS_TOKEN'
    res = requests.post(url, data=json.dumps(params), headers=headers).json()
    return res


def reserve_state_message(openId, data):
    """
            :param openId: 用户的openId
            :param data: 要发送的内容
            """
    headers = {
        'Content-Type': 'application/json'
    }
    template_id = 'FLIjh95XJrOzgWWImzmXttYhs4eoCf9e6VAid0QjHbI'
    params = {
        'access_token': access_token,
        'touser': openId,
        'template_id': template_id,
        'data': data
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=ACCESS_TOKEN'
    res = requests.post(url, data=json.dumps(params), headers=headers).json()
    return res


if __name__ == '__main__':
    pass
