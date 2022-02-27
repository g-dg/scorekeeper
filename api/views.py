from django.shortcuts import render
from django.http import HttpResponse
from scorekeeper.settings import APP_VERSION

# Create your views here.


def index(request):
    return HttpResponse(APP_VERSION)
