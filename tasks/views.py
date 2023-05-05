from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #formularios de django que se crean predeterminados bastante utiles 
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm #taskform es un formato de formulario creado en base al model task
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def duration_hours(init_time, finish_time):
    if finish_time == None or init_time>finish_time:
        return 0, 0
    finish_minutes = finish_time.hour*60 + finish_time.minute
    init_minutes = init_time.hour*60 + init_time.minute
    return int((finish_minutes-init_minutes)/60), int((finish_minutes-init_minutes)%60)

def totalHorasMes(tasks):
    contH = 0
    contm = 0
    for task in tasks:
        contH += task.durationH
        contm += task.durationm
    if contm>60:
        aux = contm/60
        contH += aux
        contm = contm%60
    return int(contH), contm

def home(request):
    return render(request, 'home.html')

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save() #hasta ahora solo se guarda en la base de datos, debemos crear una cookie para el manejo de autenticacion
                login(request, user)
                return redirect('tasks') #llama a toda la funcion tasks definida mas abajo?
                #return render(request, 'tasks.html') #solo llamaria a tsks.html??
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })
    
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user) #recupera los tasks que corresponden al usuario actual de la sesion y que su datecompleted es null, es decir q aun no han sido culminadas
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request, m, d, y):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm,
            'month': m,
            'day': d,
            'year': y
        })
    else:
        try:
            form = TaskForm(request.POST)#crea un  formulario con ese formato a partir de los datos que fueron enviados
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.month = m
            new_task.day = d
            new_task.year = y
            new_task.durationH, new_task.durationm = duration_hours(new_task.init_time, new_task.finish_time)
            new_task.save()
            tasks = Task.objects.filter(user=request.user, month=m, day=d, year=y)
            return render(request, 'tasks_by_day.html',{
                'month': m,
                'day': d,
                'year': y,
                'tasks': tasks
            })
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error': 'Please provide valid data'
            })

@login_required
def task_detail(request, m,d,y, task_id):
    if request.method == 'GET':
        #task = Task.objects.get(pk=task_id)
        task = get_object_or_404(Task, pk=task_id, user=request.user)#solo busca la tarea con el id seleccionado y si es del usuario actual
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html',{
            'task':task,
            'form': form,
            'month': m,
            'day': d,
            'year': y,
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            updated_task = form.save(commit=False)
            updated_task.durationH, updated_task.durationm = duration_hours(updated_task.init_time, updated_task.finish_time)
            #form.save()
            updated_task.save()
            return redirect('day', m,d,y)
        except ValueError:
            return render(request, 'task_detail.html',{
                'task':task,
                'form': form,
                'error': 'Error updating task'
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request,m,d,y, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('day', m,d,y)

@login_required
def signout(request):
    logout(request) #simplemente con esta vista se cierra la sesion
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
        })
    else:
        #se devuelve un usuario si la autenticacion es valida
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None: #significa que no se pudo encontrar al usuario o no es valido
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else: 
            login(request, user) #se guarda la sesion del usuario
            return redirect('tasks')
@login_required        
def calendar(request):
    return render(request, 'calendar.html')

def my_job(request):
    if request.method == 'GET':
        return render(request, 'my_job.html')
    else:
        #listaGrande = [[],[]]
        tasks = Task.objects.filter(user=request.user, month=str(request.POST.get('month')), year=int(request.POST.get('year'))).order_by('day')
        totalHoras, totalminutos = totalHorasMes(tasks)
        '''
        for i in range(1,6):
            tasksj =Task.objects.filter(user=request.user, job=i, month=str(request.POST.get('month')), year=int(request.POST.get('year')))
            totalHorasj, totalminutosj = totalHorasMes(tasksj)
            percentj = round((100/(totalHoras*60+totalminutos))*(totalHorasj*60+totalminutosj))
            listaGrande[i][0] = totalHorasj
            listaGrande[i][1] = totalminutosj
            listaGrande[i][2] = percentj
        print(listaGrande)
        '''
        tasksj1 = Task.objects.filter(user=request.user, job=1, month=str(request.POST.get('month')), year=int(request.POST.get('year')))
        totalHorasj1, totalminutosj1 = totalHorasMes(tasksj1)
        tasksj2 = Task.objects.filter(user=request.user, job=2, month=str(request.POST.get('month')), year=int(request.POST.get('year')))
        totalHorasj2, totalminutosj2 = totalHorasMes(tasksj2)
        tasksj3 = Task.objects.filter(user=request.user, job=3, month=str(request.POST.get('month')), year=int(request.POST.get('year')))
        totalHorasj3, totalminutosj3 = totalHorasMes(tasksj3)
        tasksj4 = Task.objects.filter(user=request.user, job=4, month=str(request.POST.get('month')), year=int(request.POST.get('year')))
        totalHorasj4, totalminutosj4 = totalHorasMes(tasksj4)
        tasksj5 = Task.objects.filter(user=request.user, job=5, month=str(request.POST.get('month')), year=int(request.POST.get('year')))
        totalHorasj5, totalminutosj5 = totalHorasMes(tasksj5)
        try:
            percentj1 = round((100/(totalHoras*60+totalminutos))*(totalHorasj1*60+totalminutosj1))
            percentj2 = round((100/(totalHoras*60+totalminutos))*(totalHorasj2*60+totalminutosj2))
            percentj3 = round((100/(totalHoras*60+totalminutos))*(totalHorasj3*60+totalminutosj3))
            percentj4 = round((100/(totalHoras*60+totalminutos))*(totalHorasj4*60+totalminutosj4))
            percentj5 = round((100/(totalHoras*60+totalminutos))*(totalHorasj5*60+totalminutosj5))
        except ZeroDivisionError:
            return render(request, 'my_job.html')

        return render(request, 'my_job.html',{
            'tasks': tasks,
            'totalHoras':totalHoras,
            'totalminutos':totalminutos,
            'totalHorasj1':totalHorasj1,
            'totalminutosj1':totalminutosj1,
            'totalHorasj2':totalHorasj2,
            'totalminutosj2':totalminutosj2,
            'totalHorasj3':totalHorasj3,
            'totalminutosj3':totalminutosj3,
            'totalHorasj4':totalHorasj4,
            'totalminutosj4':totalminutosj4,
            'totalHorasj5':totalHorasj5,
            'totalminutosj5':totalminutosj5,
            'percentj1':percentj1,
            'percentj2':percentj2,
            'percentj3':percentj3,
            'percentj4':percentj4,
            'percentj5':percentj5,
        })


@login_required        
def day(request, m,d,y):
    tasks = Task.objects.filter(user=request.user, month=m, day=d, year=y)
    return render(request, 'tasks_by_day.html',{
        'month': m,
        'day': d,
        'year': y,
        'tasks': tasks
    })