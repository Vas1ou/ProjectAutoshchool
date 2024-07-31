from django.http import HttpResponse
from django.shortcuts import render


def mytestview(request):
    return HttpResponse('<h1>Заглушка</h1>')
