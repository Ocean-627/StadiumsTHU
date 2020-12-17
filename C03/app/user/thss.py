import requests
import json


def login(token):
    """
    发送code并获取微信服务器响应
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
