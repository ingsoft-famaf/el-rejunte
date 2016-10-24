from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        is_active = not(self.cleaned_data["is_active"])
        return is_active
