from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from app.utils import *


def test(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    return JsonResponse({'test': 'just for test'})


def fake(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    # 清空此前的场馆信息
    clearDatabase()
    # 创建场馆
    for info in stadiums:
        initStadium(info)
    return JsonResponse({'message': 'ok'})

