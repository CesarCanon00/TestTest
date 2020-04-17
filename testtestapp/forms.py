from django.forms import ModelForm
from django.forms import TextInput, DateInput
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

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
