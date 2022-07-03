from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from .models import Room, Topic, Messages
from .forms import Form


def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, "base/room.html", context)

def createRoom(request):
    form = Form()

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = { 'form':form }
    return render(request, "base/createRoom.html", context)

