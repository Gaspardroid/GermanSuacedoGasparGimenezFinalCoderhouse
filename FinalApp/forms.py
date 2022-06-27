from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

class FormularioCompra (forms.Form):
    producto= forms.CharField()
    precio= forms.FloatField()
    
    
class FormularioRegistro (UserCreationForm):  
    
    username= forms.CharField(label= 'Usuario')
    password1= forms.CharField(label= 'Contraseña', widget=forms.PasswordInput)
    password2= forms.CharField(label= 'Repetir Contraseña', widget=forms.PasswordInput)
    email= forms.EmailField(label= 'Email')
    
    class Meta:
        model= User
        fields= ['username', 'password1', 'password2', 'email']   
        
        
  
class EditarUsuarioForm (UserCreationForm):  
    
    password1= forms.CharField(label= 'Contraseña', widget=forms.PasswordInput)
    password2= forms.CharField(label= 'Repetir Contraseña', widget=forms.PasswordInput)
    email= forms.EmailField(label= 'Email')
    first_name= forms.CharField(label= 'Nombre')
    last_name= forms.CharField(label= 'Apellido')
    
    class Meta:
        model= User
        fields= ['first_name','last_name','email','password1', 'password2']   
  

class FormularioProveedor (forms.Form):
    nombre= forms.CharField(max_length=20)
    tipo= forms.CharField(max_length=20)
    email= forms.EmailField()
    
class FormularioAvatar (forms.Form):
    avatar = forms.ImageField()