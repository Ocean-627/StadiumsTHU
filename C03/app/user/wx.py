import requests
import json

appid = ''
secret = ''


def login(js_code):
    """
    发送code并获取微信服务器响应
    """
    params = {
        'appid': appid,
        'secret': secret,
        'js_code': js_code,
        'grant_type': 'authorization_code'
    }
    url = "https://api.weixin.qq.com/sns/jscode2session"
    res = requests.get(url, params=params, verify=True)
    res.encoding = 'utf-8'
    return json.loads(res.text)
