from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from app.models import *


def test(request):
    if request.method == 'POST':
        return JsonResponse({'test': 'just for test'})


def userLogon(request):
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


def managerLogon(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    userId = request.POST.get('userId', '')
    # TODO:额外定义函数进行参数检查，这里只检查了不为空
    if not username or not password or not email or not userId:
        return JsonResponse({'error': 'Incomplete information'})
    manager = Manager(username=username, password=password, email=email, userId=userId)
    manager.save()
    return JsonResponse({'message': 'ok'})
