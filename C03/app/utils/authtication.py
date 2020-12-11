from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.utils.timezone import now
from app.models import *

# 过期时间
EXPIRED_TIME = 10


class UserAuthtication(BaseAuthentication):
    """
    验证用户身份
    """

    def authenticate(self, request):
        loginToken = request.headers.get('loginToken')
        if not loginToken:
            raise AuthenticationFailed({'error': 'Requires loginToken'})
        obj = User.objects.filter(loginToken=loginToken).first()
        if not obj:
            raise AuthenticationFailed({'error': 'Invalid loginToken'})
        now_time = now()
        if(now_time - obj.loginTime).days > EXPIRED_TIME:
            raise AuthenticationFailed({'error': 'Login timeout'})
        return obj, loginToken


class ManagerAuthtication(BaseAuthentication):
    """
    验证管理员身份
    """

    def authenticate(self, request):
        loginToken = request.COOKIES.get('loginToken')
        if not loginToken:
            raise AuthenticationFailed({'error': 'Requires loginToken'})
        obj = Manager.objects.filter(loginToken=loginToken).first()
        if not obj:
            raise AuthenticationFailed({'error': 'Invalid loginToken'})
        return obj, loginToken
