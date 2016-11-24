from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from django.core.files.images import get_image_dimensions

from .models import *


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


class DeactivateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(DeactivateUserForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = "Check this box if you are sure you want to deactivate this account."

    def clean_is_active(self):
        # Reverses true/false for your form prior to validation
        #
        # You can also raise a ValidationError here if you receive
        # a value you don't want, to prevent the form's is_valid
        # method from return true if, say, the user hasn't chosen
        # to deactivate their account
        is_active = not (self.cleaned_data["is_active"])
        return is_active


class DateInput(forms.DateInput):
    input_type = 'date'


class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('name', 'colour',)
        # widgets = {
        #     'colour': Choises(),
        # }

    def __init__(self, *args, **kwargs):
        super(NewCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = 'ingresar nombre de meta'
        self.fields['colour'].help_text = 'Selecciona el color'

    def save(self, commit=True):
        cat = super(NewCategoryForm, self).save(commit=False)
        cat.name = self.cleaned_data["name"]
        if commit:
            cat.save()
        return cat


class AddGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('name', 'finishdate', 'category', 'priority', 'file')

    def __init__(self, *args, **kwargs):
        super(AddGoalForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Ingresar meta'
        self.fields['category'].help_text = 'Ingresa categoria'
        self.fields['finishdate'].widget = widgets.AdminTimeWidget()
        for key in self.fields:
            self.fields[key].required = True
        self.fields['file'].required = False

    def save(self, commit=True):
        goal = super(AddGoalForm, self).save(commit=False)
        goal.name = self.cleaned_data["name"]
        goal.creationdate = now()
        goal.finishdate = widgets.AdminTimeWidget()
        goal.finishdate = self.cleaned_data["finishdate"]
        goal.state = "inprogress"
        goal.priority = self.cleaned_data["priority"]
        if commit:
            goal.save()
        return goal

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('profile_photo',)

    def __init__(self, *args, **kwars):
        super(MyUserForm, self).__init__(*args, **kwars)

    def save(self, commit=True):
        myuser = super(MyUserForm, self).save(commit=False)
        myuser.profile_photo = self.cleaned_data["profile_photo"]
        if commit:
            myuser.save()
        return myuser

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def __init__(self, *args, **kwars):
        super(EditProfileForm, self).__init__(*args, **kwars)

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class AddSubgoalForm(forms.ModelForm):
    class Meta:
        model = Subgoal
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(AddSubgoalForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Ingresar submeta'

    def save(self, commit=True):
        subgoal = super(AddSubgoalForm, self).save(commit=False)
        subgoal.name = self.cleaned_data["name"]
        subgoal.state = False
        if commit:
            subgoal.save()
        return subgoal

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super(AddCommentForm, self).save(commit=False)
        comment.content = self.cleaned_data["content"]
        if commit:
            comment.save()
        return comment

class GoalFilterForm(forms.Form):
    estadoChoices = (
        ('', 'Todas'),
        ('inprogress', 'En Progreso'),
        ('done', 'Terminadas'),
        ('fail', 'Falladas'),
    )
    # categoryList = ()

    nombre = forms.CharField(required=False, label='Nombre')
    estado = forms.ChoiceField(required=False, label='Estado', choices=estadoChoices)
    fechainicio = forms.DateField(required=False, label='Inicio', widget=forms.TextInput(attrs={'class': 'datepicker'}))
    fechafin = forms.DateField(required=False, label='Fin', widget=forms.TextInput(attrs={'class': 'datepicker'}))
    categoria = forms.ModelChoiceField(required=False, label='Categoria', queryset=None)

    def __init__(self, owner, *args, **kwargs):
        super(GoalFilterForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(owner=owner)




# class NewCategoryForm(forms.ModelForm):
#     class Meta:
#         model = Categoria
#         fields = ('_name', '_colour')
#
#     def __init__(self, name, owner, *args, **kwargs):
#         self.name = name
#         self.owner = owner
#         self.colour = forms.ChoiceField(choices=defaultColourList)
#         #super(NewCategoryForm, self).__init__(self.name, self.owner, self.colour)
#         #self.exclude('_owner')
#
#     def save(self, commit=True):
#         new_cat = super(NewCategoryForm, self).save(commit=False)
#         new_cat.owner = self.owner
#         new_cat.name = self.name
#         new_cat.colour = self.colour
