from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import path, reverse
from .forms import CreateUserForm, LoginUserForm, CreateTestForm
from testtestapp.models import Usuario, Test, Pregunta, Opcion, Resultado
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate

# Create your views here.

INFO = {
        'test':{
            'form':CreateTestForm,
            'name':'Test',
            'model':Test,
            'pk':'id',
        },
       }

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            usuario = Usuario(form.cleaned_data['username'],form.cleaned_data['email'],0,form.cleaned_data['birthday'])
            usuario.save()

            return HttpResponseRedirect(reverse('auth:login'))

    context = {'form':form}
    return render(request,'main/auth/register.html',context)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))
    else:
        form = LoginUserForm()
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    do_login(request, user)
                    return HttpResponseRedirect(reverse('main:home'))

        context = {'form':form}
        return render(request, "main/auth/login.html",context)

def logout(request):
    do_logout(request)
    return HttpResponseRedirect(reverse('auth:login'))

def Home(request):
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(pk=request.user.username)
        tests_usuario = Test.objects.filter(creador=usuario).order_by('fecha_test')
        context = {'usuario':usuario,'tests':tests_usuario}
        return render(request, "main/home.html",context)
    else:
        return HttpResponseRedirect(reverse('auth:login'))

def testview(request,user,idtest):
    test = Test.objects.get(pk=idtest)
    preguntas = Pregunta.objects.filter(test=idtest)
    opciones = []

    for pregunta in preguntas:
        opciones_pregunta = Opcion.objects.filter(pregunta=pregunta)
        opciones.append(opciones_pregunta)
    context = {'test':test,'preguntas':preguntas,'opciones':opciones}
    return render(request, "main/testview.html",context)

def insert(request,model):
    model_name = INFO[model]['name']
    form = INFO[model]['form']
    if request.method == 'POST':
        form = INFO[model]['form'](request.POST)
        if form.is_valid():
            creador = '{}'.format(form.cleaned_data['creador'])
            if creador == request.user.username:
                form.initial['creador'] = request.user.username
                form.save()
                return HttpResponseRedirect(reverse('main:home'))
            else:
                context= {'form': form,'error': 'El usuario ingresado no es el usuario actual.'}
                return render(request, "main/insert.html",context)
        else:
            context= {'form': form,'error': 'Datos incorrectos o mal ingresados. Intente de nuevo.'}
            return render(request, "main/insert.html",context)

    context = {'form':form,'model_name':model_name}
    
    return render(request, "main/insert.html",context)


def update(request,model,id):
    model_name = INFO[model]['name']
    obj= get_object_or_404(INFO[model]['model'], pk=id)
    form = INFO[model]['form'](request.POST or None, instance= obj)

    if request.method == 'POST':
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            context = {'form':form,'model_name':model_name,'id':id}
            return HttpResponseRedirect(reverse('main:home'))
        else:
            context= {'form': form,
            'error': 'The form was not updated successfully. Please enter in a title and content'}
            return render(request, "main/modify.html",context)

    context = {'form':form,'model_name':model_name,'id':id}
    return render(request, "main/update.html",context)

def delete(request,model,id):
    model_name = INFO[model]['name']

    if request.method == 'POST':
        INFO[model]['model'].objects.get(pk=id).delete()
        return HttpResponseRedirect(reverse('main:home'))
    else:
        context = {'model_name':model_name,'id':id}
        return render(request, "main/delete.html",context)

    context = {'model_name':model_name,'id':id}
    return render(request, "main/delete.html",context)

def results(request,id):
    if request.user.is_authenticated:
        current_user = Usuario.objects.get(pk = request.user.username)
        results_user = Resultado.objects.filter(usuario = id)
        context = {'usuario':current_user,'resultados':results_user}
        return render(request, "main/myResultsView.html",context)
    else:
        return HttpResponseRedirect(reverse('auth:login'))





   



