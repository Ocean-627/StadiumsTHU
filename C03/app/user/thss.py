import requests
import json


def login(token):
    """
    从身份认证程序获取个人信息
    """
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'token': token,
    }
    url = "https://alumni-test.iterator-traits.com/fake-id-tsinghua-proxy/api/user/session/token"
    res = requests.post(url, data=json.dumps(params), headers=headers).json()
    return res
