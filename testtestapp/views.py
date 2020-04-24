from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import path, reverse
from .forms import CreateUserForm, LoginUserForm, CreateTestForm, CreatePreguntaForm, CreateOpcionForm
from testtestapp.models import Usuario, Test, Pregunta, Opcion, Resultado, Opcion
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
        'pregunta':{
            'form':CreatePreguntaForm,
            'name':'Pregunta',
            'model':Pregunta,
            'pk':'id',
        },
        'opcion':{
            'form':CreateOpcionForm,
            'name':'Opcion',
            'model':Opcion,
            'pk':'id',
        },
       }

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            usuario = Usuario(nombre=form.cleaned_data['username'],correo=form.cleaned_data['email'],test_creados=0,fecha_nacimiento=form.cleaned_data['birthday'])
            usuario.save()
            form.save()
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

        queryset = request.GET.get("Buscar")
        print(queryset)
        
        if queryset:
            tests = Test.objects.filter(id = queryset)
            return render(request,'main/listar.html',{'tests':tests})
        usuario = Usuario.objects.get(nombre=request.user.username)
        tests_usuario = Test.objects.filter(creador=usuario).order_by('fecha_test')
        context = {'usuario':usuario,'tests':tests_usuario}
        return render(request, "main/home.html",context)
    else:
        return HttpResponseRedirect(reverse('auth:login'))

def testview(request,user,idtest):
    usuario = Usuario.objects.get(nombre=user)
    test = Test.objects.get(pk=idtest)
    preguntas = Pregunta.objects.filter(test=idtest)
    opciones = []

    for pregunta in preguntas:
        opciones_pregunta = Opcion.objects.filter(pregunta=pregunta)
        opciones.append(opciones_pregunta)
        print(opciones)
    context = {'test':test,'creador':'{}'.format(test.creador),'preguntas':preguntas,'user':usuario,'opciones':opciones}
    return render(request, "main/testview.html",context)

def insert(request,model):
    model_name = INFO[model]['name']
    form = INFO[model]['form']
    if request.method == 'POST':
        form = INFO[model]['form'](request.POST)
        if form.is_valid():
            creador = '{}'.format(form.cleaned_data['creador'])
            if creador == request.user.username:
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

def insertid(request,model,id):
    model_name = INFO[model]['name']
    form = INFO[model]['form']
    if request.method == 'POST':
        form = INFO[model]['form'](request.POST)
        if form.is_valid():
            if INFO[model]['name'] == 'Test':
                creador = '{}'.format(form.cleaned_data['creador'])
                if creador == request.user.username:
                    form.initial['creador'] = request.user.username
                    form.save()
                    return HttpResponseRedirect(reverse('main:home'))
            else:
                form.save()
                return HttpResponseRedirect(reverse('main:home'))
        else:
            context= {'form': form,'error': 'Datos incorrectos o mal ingresados. Intente de nuevo.'}
            return render(request, "main/insert.html",context)

    context = {'form':form,'model_name':model_name,'id':id}
    
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

def busqueda(request):
   q = request.GET.get('q', '')
   test = Test.objects.filter(Q(nombre__icontains = q)|Q(id__icontains = q)|Q(creador__nombre__icontains = q)|Q(categoria__nombre__icontains = q)).distinct()
   return render(request, 'main/do_test.html', {'test': test})

   
def intest(request,user,idtest):
    print(request.method == 'POST')

    if request.method == 'POST':
        usuario = Usuario.objects.get(pk=user)
        preguntas = Pregunta.objects.filter(test=idtest)
        test = Test.objects.get(pk=idtest)
        resultados = Resultado.objects.filter(test=idtest,usuario=user).values('calificacion')
        print(resultados)
        
        scores = None
        if resultados:
            scores = "{}".format(resultados[0]).split("('")[1].split("')")[0]
            print(scores)

        score = 0.0
        for pregunta in preguntas:
            if request.POST.get("{}".format(pregunta.id)):
                strscore = "{}".format(request.POST.get("{}".format(pregunta.id))).replace(",",".")
                score+=float(strscore)
        resultado =  Resultado(calificacion=score,test=test,usuario=usuario).save()
    
        context = {'test':test,'creador':'{}'.format(test.creador),'user':usuario,'results':resultados,'scores':scores}
        return render(request, "main/intest.html",context)

    else:
        usuario = Usuario.objects.get(pk=user)
        test = Test.objects.get(pk=idtest)
        preguntas = Pregunta.objects.filter(test=idtest)
        resultados = Resultado.objects.filter(test=idtest,usuario=user).values('calificacion')
        scores = None
        if resultados:
            scores = "{}".format(resultados[0]).split("('")[1].split("')")[0]
            print(scores)

        opciones = []
        for pregunta in preguntas:
            opciones_pregunta = Opcion.objects.filter(pregunta=pregunta)
            opciones.append(opciones_pregunta)
            
        context = {'test':test,'creador':'{}'.format(test.creador),'preguntas':preguntas,'user':usuario,'opciones':opciones,'results':resultados,'scores':scores}
        return render(request, "main/intest.html",context)




   



