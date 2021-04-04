from django import forms
from .models import Portfolio, User, Project, ProductType

class LoginForm(forms.Form):
    email = forms.CharField(label = 'email')
    password = forms.CharField(label = 'Password')

class RegistrationForm(forms.Form):
    name = forms.CharField(label = 'Name')
    alias = forms.CharField(label = 'Username')
    email = forms.CharField(label= 'Email')
    password = forms.CharField(label='Password')
    passwordConfirm = forms.CharField(label='Password Confirmation')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']
    
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'owner']
        # widgets: {
        #     'owner': Select()
        # }

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['name', 'fractionalLotsAllowed']
        labels = {
            'name': 'Name',
            'fractionalLotsAllowed': 'Fractional Lots Allowed',
        }
