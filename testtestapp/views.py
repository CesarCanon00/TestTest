from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import path, reverse
from .forms import CreateUserForm, LoginUserForm
from testtestapp.models import Usuario, Test, Pregunta, Opcion
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate

# Create your views here.

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
        tests_usuario = Test.objects.filter(creador=usuario)
        print(tests_usuario)
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


   



