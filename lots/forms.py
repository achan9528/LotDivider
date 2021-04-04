from django import forms
from django.forms import ModelForm
from .models import *

class LoginForm(forms.Form):
    email = forms.CharField(label = 'email')
    password = forms.CharField(label = 'Password')

class RegistrationForm(forms.Form):
    name = forms.CharField(label = 'Name')
    alias = forms.CharField(label = 'Username')
    email = forms.CharField(label= 'Email')
    password = forms.CharField(label='Password')
    passwordConfirm = forms.CharField(label='Password Confirmation')
    
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']

class ProductTypeForm(ModelForm):
    class Meta:
        model = ProductType
        fields = ['name', 'fractionalLotsAllowed']
        labels = {
            'name': 'Name',
            'fractionalLotsAllowed': 'Fractional Lots Allowed',
        }

class SecurityForm(ModelForm):
    class Meta:
        model = Security
        fields = ['ticker','cusip','name','productType']
        labels = {
            'ticker': 'Ticker',
            'cusip': 'CUSIP',
            'name': 'Name',
            'productType': 'Product Type',
        }

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'owner']
        # widgets: {
        #     'owner': Select()
        # }

class HoldingForm(ModelForm):
    class Meta:
        model = Holding
        fields = ['security', 'account']
        labels = {
            'security': 'Security',
            'account': 'Account',
        }

class TaxLotForm(ModelForm):
    class Meta:
        model = TaxLot
        fields = ['holding', 'units', 'totalFederalCost', 'totalStateCost']
        labels = {
            'holding': 'Holding',
            'units': 'Units',
            'totalFederalCost': 'Total Federal Cost',
            'totalStateCost': 'Total State Cost',
        }

class DraftPortfolioForm(ModelForm):
    class Meta:
        model = DraftPortfolio
        fields = ['name', 'project']

class DraftAccountForm(ModelForm):
    class Meta:
        model = DraftAccount
        fields = ['name','draftPortfolio']

class DraftHoldingForm(ModelForm):
    class Meta:
        model = DraftHolding
        fields = ['security', 'draftAccount']

class DraftTaxLotForm(ModelForm):
    class Meta:
        model = DraftTaxLot
        fields = ['draftHolding', 'units', 'totalFederalCost', 'totalStateCost']
        labels = {
            'draftHolding': 'Holding',
            'units': 'Units',
            'totalFederalCost': 'Total Federal Cost',
            'totalStateCost': 'Total State Cost',
        }