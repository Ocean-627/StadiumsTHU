from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from app.models import *


class UserAuthtication(BaseAuthentication):
    """
    验证用户身份
    """

    def authenticate(self, request):
        # TODO:目前将身份验证放在头部，实际上小程序端应该通过request.META.get()来获取
        loginToken = request.GET.get('loginToken')
        if not loginToken:
            raise AuthenticationFailed({'error': 'Requires loginToken'})
        obj = User.objects.filter(loginToken=loginToken).first()
        if not obj:
            raise AuthenticationFailed({'error': 'Invalid loginToken'})
        return obj, loginToken


class ManagerAuthtication(BaseAuthentication):
    """
    验证管理员身份
    """

    def authenticate(self, request):
        if 'Cookie' not in request.headers:
            raise AuthenticationFailed({'error': 'Requires loginToken'})
        loginToken = request.headers['Cookie'].split('=')[1]
        if not loginToken:
            raise AuthenticationFailed({'error': 'Requires loginToken'})
        obj = Manager.objects.filter(loginToken=loginToken).first()
        if not obj:
            raise AuthenticationFailed({'error': 'Invalid loginToken'})
        return obj, loginToken