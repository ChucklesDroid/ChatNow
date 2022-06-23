from django.shortcuts import render
from djang.http import HttpResponse

def home(request):
    return HttpResponse("Home")

def room(request):
    return HttpResponse("Home")

