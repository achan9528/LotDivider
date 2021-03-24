from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .services import *

# Create your views here.
def index(request):
    if request.method=='GET':
        context = {
            
        }
        return render(request, "index.html", context)
    elif request.method=='POST':
        return "this is a test"
        
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
                name = request.POST['name']
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

def viewLots(request):
    if request.method=='GET':        
        context = {
            "portfolio":Portfolio.objects.first()
        }
        return render(request, "lots.html", context)

def split(request):
    if request.method=='GET':
        getShares()
        return HttpResponse("test")  

