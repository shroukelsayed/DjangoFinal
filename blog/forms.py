from django.contrib.auth.models import User
from django.db import models
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields=('username','email','password')


#ForgetPassword Part -->shrouk(classes : forgetPassForm ,confirmPassForm)
class forgetPassForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs=dict(required=True,placeholder="Plz Enter Your Username...")))
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True,placeholder="Plz Enter Your Mail...")))
 
class confirmPassForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(attrs=dict(required=True,max_length=10,placeholder="Plz Confirmation Code...")))
 
class resetPassForm(forms.Form):
	password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs=dict(required=True,placeholder="Plz Enter Your Password...")))
	confirmPassword = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs=dict(required=True,placeholder="Plz Enter Your Password Again...")))
 