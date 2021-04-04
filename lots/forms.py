from django import forms
from .models import Portfolio

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username')
    password = forms.CharField(label = 'Password')

class RegistrationForm(forms.Form):
    name = forms.CharField(label = 'Name')
    alias = forms.CharField(label = 'Nickname')
    username = forms.CharField(label = 'Username')
    password = forms.CharField(label = 'Password')
    passwordConfirm = forms.CharField(label = 'Password Confirmation')

class ProjectForm(forms.Form):
    name = forms.CharField(label = 'Project Name')
    
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'owner']
        # widgets: {
        #     'owner': Select()
        # }