from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from app.utils.user_serializer import *
from app.utils.utils import *

import base64


def test(request):
    return JsonResponse({'test': 'just for test'})
