from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import *
from . import queries as LotQueries
from . import services as LotService
from .forms import *
from django.core.serializers import serialize
import bcrypt

def validUser(request):
    if 'userID' in request.session:
        return True
    return False

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
            return redirect("/dashboard/")

def dashboard(request):
    if validUser(request):
        if request.method == 'GET':
            # request.session['portfolioID'] = Portfolio.objects.get(name="alex").id
            context = {
                'user': User.objects.get(id=request.session['userID']),
                'projects': User.objects.get(id=request.session['userID']).projects.all(),
            }
            return render(request, "dashboard.html", context)
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def newProject(request):
    if validUser(request):
        if request.method == 'GET':
            form = ProjectForm()
            context = {
                'newProjectForm': form,
            }
            return render(request, "newProject.html", context)
        if request.method == 'POST':
            # formData = ProjectForm(request.POST)
            # errors = Project.objects.createValidator(formData)
            # errors = Project.objects.createValidator(request.POST)
            # if len(errors) > 0:
            #     for key,value in errors.items():
            #         messages.error(request, value)
            #     return redirect('/projects/new/')
            # else:
                newProject = Project.objects.create(
                    name = request.POST['name'],
                )
                newProject.owners.add(User.objects.get(id=request.session['userID']))
                newProject.save()
                return redirect("/projects/" + str(newProject.id) + "/")
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def projectDashboard(request, id):
    if validUser(request):
        if request.method == 'GET':
            project = Project.objects.get(id=id)
            # portfolios = Portfolio.objects.all()
            portfolios = []
            # for proposal in project.proposals.all():
            #     num = proposal.draftPortfolios.first().draftAccounts.first().draftHoldings.first().draftTaxLots.first().number
            #     portfolio = TaxLot.objects.get(number=num).holding.account.portfolio
            #     if portfolio not in portfolios:
            #         portfolios.append(portfolio)
            context = {
                'project': project,
                # 'portfolios': portfolios,
            }
            return render(request, 'projectDashboard.html', context)
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def selectPortfolio(request, projectID):
    if validUser(request):
        if request.method == 'GET':
            project = Project.objects.get(id=projectID)
            portfolios = Portfolio.objects.all()
            context = {
                'project': project,
                'portfolios': portfolios,
            }
            return render(request, 'portfolios.html', context)
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def portfolioView(request, projectID, portfolioID):
    if validUser(request):
        if request.method == 'GET':
            context = {
                'project': Project.objects.get(id=projectID),
                'portfolio': Portfolio.objects.get(id=portfolioID),
                'accounts': Portfolio.objects.get(id=portfolioID).accounts.all()
            }
            return render(request, 'portfolioView.html', context)
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def accountView(request, projectID, portfolioID, accountID):
    if validUser(request):
        if request.method == 'GET':
            context = {
                'project': Project.objects.get(id=projectID),
                'portfolio': Portfolio.objects.get(id=portfolioID),
                'account': Account.objects.get(id=accountID),
                "holdings" : LotService.getHoldings(accountID),
                "orderedHoldings": LotService.getHoldings(accountID).sort(key=lambda x:x["name"])
            }
            return render(request, 'accountView.html', context)
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def newProposal(request, projectID, portfolioID, accountID):
    if validUser(request):
        if request.method == 'GET':
            context = {
                'project': Project.objects.get(id=projectID),
                'portfolio': Portfolio.objects.get(id=portfolioID),
                'account': Account.objects.get(id=accountID),
                "holdings" : LotService.getHoldings(accountID),
                "orderedHoldings": LotService.getHoldings(accountID).sort(key=lambda x:x["name"])
            }
            return render(request, 'newProposal.html', context)
        if request.method=='POST':
            print(request.POST)
            holdingsDict = {}
            for holding in Account.objects.get(id=accountID).holdings.all():
                if holding.security.ticker in request.POST and len(request.POST[holding.security.ticker]) > 0:
                    if Decimal(request.POST[holding.security.ticker]) > 0:
                        holdingsDict[holding.security.ticker] = request.POST[holding.security.ticker]
            # proposal = LotService.splitPortfolio(
            #     projectID=projectID,
            #     accountID=accountID,
            #     method=request.POST["method"],
            #     numberOfPortfolios=request.POST["numberOfPortfolios"],
            #     holdingsDict=holdingsDict,
            # )
            proposal2 = LotService.splitPortfolio2(
                projectID=projectID,
                accountID=accountID,
                method=request.POST["method"],
                numberOfPortfolios=request.POST["numberOfPortfolios"],
                holdingsDict=holdingsDict,
            )
            
            # return redirect('/projects/' + str(projectID) + '/portfolios/' + str(portfolioID) + '/accounts/' + str(accountID) + '/proposals/new')
            return redirect('/proposals/' + str(proposal2.id) + "/")
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def viewProposal(request, proposalID):
    if validUser(request):
        if request.method == 'GET':
            proposalSummary = LotQueries.summarizeProposal(Proposal.objects.get(id=proposalID))
            context = {
                'proposal': Proposal.objects.get(id=proposalID),
                'proposalSummary': proposalSummary,
                'test': {'test': 'test','test2':{'test3':'test3'}},
            }
            LotQueries.test(proposalID)
            return render(request, 'proposal.html', context)

    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def editProposal(request, proposalID):
    if validUser(request):
        if request.method == 'GET':
            context = {
                'proposal': Proposal.objects.get(id=proposalID)
            }
            return render(request, 'editProposal.html', context)
        if request.method == 'POST':
            proposal = Proposal.objects.get(id=proposalID)
            proposal.name = request.POST['proposalName']
            proposal.save()
            return redirect('/proposals/' + str(proposalID) + '/')
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def deleteProposal(request, proposalID):
    if validUser(request):
        if request.method == 'GET':
            context = {
                'proposal': Proposal.objects.get(id=proposalID)
            }
            return render(request, 'deleteProposal.html', context)
        if request.method == 'POST':
            if request.POST['_method'] == 'delete':
                projectID = Proposal.objects.get(id=proposalID).project.id
                Proposal.objects.get(id=proposalID).delete()
                return redirect('/projects/' + str(projectID) + '/')    
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def newPortfolio(request):
    if validUser(request):
        if request.method == 'GET':
            context = {

            }
            return render(request, 'newPortfolio.html', context)
        # if request.method == 'POST':
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

def test(request):
    if validUser(request):
        if request.method == 'POST':
            print(request.FILES)
            print(request.FILES['fileUpload'])
            LotService.uploadPortfolio(request.FILES['fileUpload'], request.POST['portfolioName'], request.POST['accountName'])
            return redirect('/portfolios/new')
        # if request.method == 'POST':
    else:
        messages.error(request, 'Please login!')
        return redirect('/')

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
            return redirect('/admin')

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
                portfolio = Portfolio.objects.get(name=request.POST['portfolioName']),
            )
            return redirect('/admin')

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
            return redirect('/admin')

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
            return redirect('/admin')

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
                account = Portfolio.objects.get(name=request.POST['holdingPortfolio']).
                accounts.get(name=request.POST['holdingAccount']),
            )
            return redirect('/admin')

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
                    account = Portfolio.objects.get(name=request.POST['portfolio']).
                    accounts.get(name=request.POST['account'])
                ), units = request.POST['units'],
                totalFederalCost = request.POST['totalFederalCost'],
                totalStateCost = request.POST['totalStateCost'],
            )
            return redirect('/admin')

def admin(request):
    return render(request, 'index.html')

def logout(request):
    request.session.clear()
    return redirect('/')