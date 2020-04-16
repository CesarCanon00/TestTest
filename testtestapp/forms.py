from django.forms import ModelForm
from django.forms import TextInput, DateInput
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username','password1','password2']