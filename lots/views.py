from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import *
from . import services as LotService
from .forms import LoginForm, RegistrationForm, PortfolioForm, ProductTypeForm
import bcrypt

def dashboard(request):
    if request.method=='GET':
        request.session['portfolioID'] = Portfolio.objects.get(name="alex").id
        context = {
            
        }
        return render(request, "index.html", context)
    elif request.method=='POST':
        return "this is a test"

def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'registrationPage.html', context)
    if request.method == 'POST':
        errors = User.objects.registrationValidator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
                print(value)
            return redirect("/register")
        else:
            password = request.POST['password']
            pwHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(
                name=request.POST["name"],
                alias=request.POST["alias"],
                email=request.POST["email"],
                password=pwHash
            )
            request.session["userID"] = newUser.id
            return redirect("/dashboard")

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        form2 = PortfolioForm()
        form3 = ProductTypeForm()
        context = {
            'form': form,
            'form2': form2,
            'form3': form3,
        }
        return render(request, 'loginPage.html', context)

    if request.method == 'POST':
        print('HERE IS THE REQUEST DATA:')
        print(request.POST)
        errors = User.objects.loginValidator(request.POST)
        users = User.objects.filter(email=request.POST['email'])
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
                print(value)
            return redirect ("/login")
        elif users:
            logged_user = users[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userID'] = logged_user.id
                return redirect("/dashboard")
            else:
                messages.error(request,"Password does not match!")
                return redirect("/login")
        
def addPortfolio(request):
    print(request)
    if request.method=='POST':
        # errors = Portfolio.objects.portfolioValidator(request.POST)
        # if len(errors) > 0:
        #     for key,value in errors.items():
        #         messages.error(request,value)
        #     return redirect("/")
        # else:
            newPortfolio = Portfolio.objects.create(
                name = request.POST['name'],
                owner= User.objects.get(name="alex"),
            )
            return redirect('/')

def addAccount(request):
    print(request)
    if request.method=='POST':
        # errors = Portfolio.objects.portfolioValidator(request.POST)
        # if len(errors) > 0:
        #     for key,value in errors.items():
        #         messages.error(request,value)
        #     return redirect("/")
        # else:
            newAccount = Account.objects.create(
                name = request.POST['accountName'],
                portfolio = Portfolio.objects.get(name="alex"),
            )
            return redirect('/')

def addProductType(request):
    print(request)
    if request.method=='POST':
        # errors = Portfolio.objects.portfolioValidator(request.POST)
        # if len(errors) > 0:
        #     for key,value in errors.items():
        #         messages.error(request,value)
        #     return redirect("/")
        # else:
            newProducType = ProductType.objects.create(
                name = request.POST['productTypeName'],
                # fractionalLotsAllowed = boolean(request.POST['productTypeFractionalLotsAllowed'].lower()=='true'),
            )
            return redirect('/')

def addSecurity(request):
    print(request)
    if request.method=='POST':
        # errors = Portfolio.objects.portfolioValidator(request.POST)
        # if len(errors) > 0:
        #     for key,value in errors.items():
        #         messages.error(request,value)
        #     return redirect("/")
        # else:
            newSecurity = Security.objects.create(
                name = request.POST['securityName'],
                cusip = request.POST['securityCusip'],
                ticker = request.POST['securityTicker'],
                productType = ProductType.objects.get(name=request.POST['securityProductType'])
            )
            return redirect('/')

def addHolding(request):
    print(request)
    if request.method=='POST':
        # errors = Portfolio.objects.portfolioValidator(request.POST)
        # if len(errors) > 0:
        #     for key,value in errors.items():
        #         messages.error(request,value)
        #     return redirect("/")
        # else:
            newHolding = Holding.objects.create(
                security = Security.objects.get(ticker=request.POST['holdingTicker']),
                account = Portfolio.objects.get(id=request.session['portfolioID']).accounts.get(
                            name=request.POST['holdingAccount'])
            )
            return redirect('/')

def addLot(request):
    print(request)
    if request.method=='POST':
        # errors = Portfolio.objects.portfolioValidator(request.POST)
        # if len(errors) > 0:
        #     for key,value in errors.items():
        #         messages.error(request,value)
        #     return redirect("/")
        # else: 
            newLot = TaxLot.objects.create(
                holding = Holding.objects.get(
                    security=Security.objects.get(ticker=request.POST['ticker']),
                    account=Portfolio.objects.get(name="alex").accounts.get(name="testAccount")
                ), units = request.POST['units'],
                totalFederalCost = request.POST['totalFederalCost'],
                totalStateCost = request.POST['totalStateCost'],
            )
            return redirect('/')

def viewAccountHoldings(request):
    if request.method=='GET':        
        context = {
            "account": Account.objects.first(),
            "holdings" : getHoldings(Account.objects.first().id),
            "orderedHoldings": getHoldings(Account.objects.first().id).sort(key=lambda x:x["name"])
        }
        return render(request, "holdings.html", context)

def viewSelectPage(request):
    if request.method=='GET':
        request.session["accountID"] = Account.objects.get(name="testAccount").id
        print(request.session["accountID"])
        context = {
            "account": Account.objects.get(name="testAccount"),
            "holdings" : LotService.getHoldings(Account.objects.get(name="testAccount").id),
            "orderedHoldings": LotService.getHoldings(Account.objects.get(name="testAccount").id).sort(key=lambda x:x["name"])
        }
        return render(request, "select.html", context)

def viewLots(request):
    if request.method=='GET':        
        context = {
            "portfolio":Portfolio.objects.first()
        }
        return render(request, "lots.html", context)

def split(request):
    if request.method=='POST':
        print(request.POST)
        holdingsDict = {}
        for holding in Account.objects.get(id=request.session['accountID']).holdings.all():
            if holding.security.ticker in request.POST and len(request.POST[holding.security.ticker]) > 0:
                if Decimal(request.POST[holding.security.ticker]) > 0:
                    holdingsDict[holding.security.ticker] = request.POST[holding.security.ticker]
        returnDict = LotService.splitPortfolio(
            accountID=request.session['accountID'],
            method=request.POST["method"],
            numberOfPortfolios=request.POST["numberOfPortfolios"],
            holdingsDict=holdingsDict,
        )
        return HttpResponse(returnDict)

def newProject(request):
    if request.method=='POST':
        # on post method, save the new Project with the current values from the form
        # validations
        # errors = Project.objects.projectValidator(request.POST)
        # if len(errors) > 0:
        #     for key,value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/')
        # else:
            Project.objects.create(
                name = request.POST['projectName'],
                # number = (default generated)
                # owners = (many to many)
            )
            return redirect('/')
        