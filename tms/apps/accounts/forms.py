from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import User, Profile, USERTYPE_CHOICES


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Username...",
                "class": "form-control form-control-user"
            }
        ))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control form-control-user"
            }
        ))


class AgentRegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Agent's First Name"
            }
        ))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': "Agent's Last Name"
            }
        ))

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': "Leave Blank for automatic username generation"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': "Enter An Active Email Address"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Password'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Confirm Password'
            }
        )
    )

    class meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ProfileInfoForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "readonly": True
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "readonly": True
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "readonly": True
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "readonly": True
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileInfoUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfilePicsUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
