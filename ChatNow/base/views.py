from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Topic, Messages
from .forms import Form
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist..")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR Password entered is incorrect...!!")


    context = { 'page':page }
    return render(request, 'base/login_register.html', context)


def registerUser(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured while logging in")

    return render(request, 'base/login_register.html', {'form':form})


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):

    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    rooms_count = rooms.count()
    topics = Topic.objects.all()

    context = {'rooms':rooms, 'topics':topics, 'rooms_count':rooms_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all()
    participants = room.participants.all()
    
    if request.method == "POST":
        Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        login(request, request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages': room_messages, 'participants':participants}
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


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = Form(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        form = Form(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {'form': form}
    return render(request, 'base/createRoom.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here...!!")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Messages.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here...!!")

    if request.method == "POST":
        message.delete()
        return redirect("home")

    return render(request, 'base/delete.html', {'obj':message})
