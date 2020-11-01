from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def test(request):
    if request.method == 'POST':
        return JsonResponse({'test': 'just for test'})

