from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from django.db.models import Q
from .models import Room, Topic, Messages
from .forms import Form


def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()

    context = {'rooms':rooms, 'topics':topics}
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

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = Form(instance=room)

    if request.method == "POST":
        form = Form(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {'form': form}
    return render(request, 'base/createRoom.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, 'base/delete.html', {'obj':room})
