import re
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import Metas
from django.forms import ModelForm


# # If you don't do this you cannot use Bootstrap CSS
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label="Username", max_length=30,
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
#     password = forms.CharField(label="Password", max_length=30,
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class AddMetaForm(ModelForm):
    
    class Meta:
        model = Metas
        fields = ('_name', '_creationdate', '_finishdate')

    def save(self, commit=True):
    	def getuser(request):
    		current_user = request.user
    	return current_user.id
        
        meta = super(AddMetaForm, self).save(commit=False)
        meta._name = self.cleaned_data["_name"]
        meta.user = getuser()
        meta._creationdate = self.cleaned_data["_creationdate"]
        meta._finishdate = self.cleaned_data["_finishdate"]
        if commit:
            meta.save()
        return meta
