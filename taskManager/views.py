from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from django.http import JsonResponse

from .models import *

# Create your views here.

def login_(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect(dashboard)
            return redirect(index)
        else:
            msg = 'Nada papi te equivocaste, dale pa ve'
            return render(request, 'login.html', {'msg':msg})
    else:
        return render(request, 'login.html')
    
def logout_(request):
    logout(request)
    return redirect(index)

@login_required(login_url='/login')
def index(request):
    if request.method == 'POST':
        task = Task()
        task.subject = request.POST['subject']
        task.user = Users.objects.filter(id=request.user.id).first()
        task.addressee = request.POST['addressee']
        task.save()
    tasks = Task.objects.filter(user_id=request.user.id)
    contex = {
        'tasks':tasks
    }
    return render(request, 'newTask.html', contex)

@login_required(login_url='/login')
def dashboard(request):
    if not request.user.is_staff:
        return redirect(index)
    if request.method == 'POST':
        answer = request.POST['answer']
        task_id = request.POST['task_id']
        task = Task.objects.get(id=task_id)
        task.date_answer = timezone.now()
        task.answer = answer
        task.save()
    userConect = str(request.user.username)
    contex = {
        'tasks':Task.objects.filter(addressee=userConect)
    }
    return render(request, 'dashboard.html', contex)

def get_tasks(request):
    tasks = Task.objects.filter(addressee=request.user).select_related('user').values(
        'id', 'subject', 'answer', 'date', 'user__id', 'user__first_name'
    )
    tasks_list = list(tasks)
    return JsonResponse({'tasks': tasks_list})