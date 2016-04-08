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
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True)))
 
class confirmPassForm(forms.Form):
	code = forms.CharField(max_length=10)
        