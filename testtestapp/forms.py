from django.forms import ModelForm
from django.forms import TextInput, DateInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from testtestapp.models import Test

class CreateUserForm(UserCreationForm):

    email = forms.EmailField(required=True)
    birthday = forms.DateField(required=True)

    class meta:
        model = User
        fields = ['username','email','password1','password2','birthday']
        labels = {'username':'Usuario',
                    'email':'Correo Electrónico',
                    'password1':'Contraseña',
                    'password2':'Repetir Contraseña',
                    'birthday':'Fecha de Nacimiento'
                 }
    
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.birthday = self.cleaned_data["birthday"]
        if commit:
            user.save()
        return user

class LoginUserForm(AuthenticationForm):
    class meta:
        model = User
        fields = ['username','password']
        labels = {
                    'username':'Usuario',
                    'password':'Contraseña'  
                 }

class CreateTestForm(ModelForm):
    class Meta:
        model = Test
        fields = ['nombre','fecha_test','duracion','maxima_puntuacion','descripcion','categoria','creador']
        labels = {'nombre': 'Nombre del Test',
                'fecha_test':'Fecha (YYYY-MM-DD)',
                'duracion':'Duración en Minutos',
                'maxima_puntuacion':'Máxima Puntuación',
                'descripcion':'Descripción',
                'categoria':'Categoría',
                'creador':'Creador'
                }

        widgets = {
            'creador': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CreateTestForm, self).__init__(*args, **kwargs)
        self.fields['creador'].required = False