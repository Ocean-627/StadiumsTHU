import requests
import json


def login(token):
    """
    发送code并获取微信服务器响应
    """
    params = {
        'token': token,
    }
    url = "https://alumni-test.iterator-traits.com/fake-id-tsinghua-proxy/api/user/session/token"
    res = requests.post(url, params=params, verify=True)
    res.encoding = 'utf-8'
    return json.loads(res.text)


if __name__ == '__main__':
    res = login('')
    print(res)
