from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from app.serializer import *
from app.utils import *


def test(request):
    img = request.FILES.get('image')
    stadium = Stadium(
        name='测试场馆',
        img=img,
        information='随便',
        openingHours='7-11,15-18',
        openTime='7:00',
        closeTime='18:00',
        contact='18801225328',
        openState=True,
        foreDays=1,
        durations='01:00'
    )
    stadium.save()
    stadium = StadiumSerializer(stadium, many=False)
    return JsonResponse({'stadium': stadium.data})


def fake(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    # 清空此前的场馆信息
    clearDatabase()
    # 创建场馆
    for info in stadiums:
        initStadium(info)
    return JsonResponse({'message': 'ok'})
