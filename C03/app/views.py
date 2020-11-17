from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from app.utils.serializer import *
from app.utils.utils import *


def test(request):
    A = '08:00'
    B = '12:00'
    return JsonResponse({'time': judgeTime(A, B)})


def fake(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    # 清空此前的场馆信息
    clearDatabase()
    # 创建场馆
    for info in stadiums:
        initStadium(info)
    return JsonResponse({'message': 'ok'})
