from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from app.utils import *


def test(request):
    ImageItem.objects.all().delete()
    img = request.FILES.get('image')
    item = ImageItem(img=img)
    item.save()
    return HttpResponse(item.img, content_type='image/jpeg')


def fake(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Requires POST'})
    # 清空此前的场馆信息
    clearDatabase()
    # 创建场馆
    for info in stadiums:
        initStadium(info)
    return JsonResponse({'message': 'ok'})

