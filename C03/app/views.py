from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from app.utils.serializer import *
from app.utils.utils import *

import base64


def test(request):
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
