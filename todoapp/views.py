from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .forms import CreateTodo
from .models import Todo
from django.utils import timezone
# Create your views here.

def index(request):
    return render(request, 'todoapp/index.html')

def usersignup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request,user)
                return render(request, 'todoapp/index.html')
            except:
                return render(request,'todoapp/signup.html', {'form':UserCreationForm(), 'error': 'Username already registered'})
        else:
            return render(request,'todoapp/signup.html', {'form':UserCreationForm(), 'error': 'Password Should be matched'})
    else:
        return render(request,'todoapp/signup.html', {'form':UserCreationForm()})

@login_required
def userlogout(request):
    logout(request)
    return redirect('index')

def userlogin(request):
    if request.method == 'POST':
        user = authenticate(username = request.POST['username'],password = request.POST['password'])
        if user is None:
            return render(request,'todoapp/login.html', {'form':AuthenticationForm(), 'error': 'invalid User'})
        else:
            login(request,user)
            return redirect('index')
    else:
        return render(request,'todoapp/login.html', {'form':AuthenticationForm()})


@login_required()
def createtodo(request):
    if request.method == 'POST':
        todo = CreateTodo(request.POST)
        newtodo = todo.save(commit = False)
        newtodo.user = request.user
        newtodo.save()
        return redirect('current')
    else:
        return render(request, 'todoapp/create.html',{'form':CreateTodo()})


@login_required()
def current(request):
    todolist = Todo.objects.filter(user = request.user, completed__isnull = True)
    return render(request,'todoapp/current.html', {'todolist':todolist})


@login_required()
def viewtodo(request, todo_id):
    todo = get_object_or_404(Todo, pk = todo_id,user = request.user)
    if request.method == 'POST':
        todo = CreateTodo(request.POST,instance = todo)
        todo.save()
        return redirect('current')
    else:
        todoform = CreateTodo(instance = todo)
        return render(request,'todoapp/viewtodo.html', {'todo':todo,'todoform':todoform})


@login_required()
def completetodo(request, todo_id):
    todo = get_object_or_404(Todo,pk=todo_id,user = request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('current')


@login_required()
def deletetodo(request, todo_id):
    todo = get_object_or_404(Todo,pk=todo_id, user = request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')


@login_required()
def showcompletedtodo(request):
    todolist = Todo.objects.filter(user = request.user, completed__isnull = False).order_by('-completed')
    return render(request,'todoapp/completedtodo.html', {'todolist':todolist})
