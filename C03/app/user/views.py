from django.http import JsonResponse
from app.models import *
import hashlib


def logon(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    userId = request.POST.get('userId', '')
    # TODO:额外定义函数进行参数检查，这里只检查了不为空
    if not username or not password or not email or not userId:
        return JsonResponse({'error': 'Incomplete information'})
    user = User(username=username, password=password, email=email, userId=userId)
    user.save()
    return JsonResponse({'message': 'ok'})



def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    userId = request.POST.get('userId', '')
    password = request.POST.get('password', '')
    try:
        userInfo = User.objects.get(userId=userId)
        # 已经登录
        if 'loginToken' in request.COOKIES:
            loginToken = request.COOKIES['loginToken']
            if loginToken == userInfo.loginToken:
                return JsonResponse({'message': 'ok'})
        if password != userInfo.password:
            return JsonResponse({'error': 'Wrong password'})
        # TODO:使用更合理的session算法
        loginToken = hashlib.sha1(userId.encode('utf-8')).hexdigest()
        userInfo.loginToken = loginToken
        userInfo.save()
        resp = JsonResponse({'message': 'ok'})
        # 设置Cookie
        resp.set_cookie('loginToken', loginToken)
        return resp
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'})


def logout(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    if 'loginToken' not in request.COOKIES:
        return JsonResponse({'error': 'Not yet logged in'})
    loginToken = request.COOKIES['loginToken']
    userInfo = User.objects.get(loginToken=loginToken)
    userInfo.loginToken = ''
    userInfo.save()
    resp = JsonResponse({'message': 'ok'})
    resp.delete_cookie('loginToke')
    return resp
