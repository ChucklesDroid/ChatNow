from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id':1, 'name':'Django Tutorials'},
    {'id':2, 'name':'Bash Scripting'},
    {'id':3, 'name':'Welcome to ChatNow'},
]

def home(request):
    return render(request, 'base/home.html', {'rooms':rooms})

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i

    return render(request, "base/room.html", {'room':room})

