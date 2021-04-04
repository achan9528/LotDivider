from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username')
    password = forms.CharField(label = 'Password')

class RegistrationForm(forms.Form):
    name = forms.CharField(label = 'Name')
    alias = forms.CharField(label = 'Nickname')
    username = forms.CharField(label = 'Username')
    password = forms.CharField(label = 'Password')
    passwordConfirm = forms.CharField(label = 'Password Confirmation')