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
            raise AuthenticationFailed({'error': 'Wrong loginToken'})
        return obj, loginToken
