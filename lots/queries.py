from django.db.models import Sum, F, Value, FloatField, ExpressionWrapper, CharField
from .models import *
import yfinance as yf

def summarizeProposal(proposal):
    summaryDict = {
        'lots': getDraftLotCPS(proposal),
        'totals': getDraftTotals(proposal),
    }
    # print(summaryDict)
    return summaryDict

def getDraftLotCPS(proposal):    
    returnDict = {}

    for draftPortfolio in proposal.draftPortfolios.all():
        for draftAccount in draftPortfolio.draftAccounts.all():
            returnDict[draftPortfolio, draftAccount] = []
            for draftHolding in draftAccount.draftHoldings.all():
                draftLots = draftHolding.draftTaxLots.annotate(cps=ExpressionWrapper(F("referencedLot__totalFederalCost")/F("referencedLot__units"),output_field=FloatField()),
                unitsAvailable=F("referencedLot__units"), totalFederalCost=F("referencedLot__totalFederalCost"))
                
                returnDict[draftPortfolio, draftAccount].append(draftLots)
    return returnDict

def getDraftTotals(proposal):
    totalsDict = {}

    for draftPortfolio in proposal.draftPortfolios.all():
        for draftAccount in draftPortfolio.draftAccounts.all():
            for draftHolding in draftAccount.draftHoldings.all():
                totalUnits = draftHolding.draftTaxLots.aggregate(totalUnits=Sum('units'))

                closingPrice = yf.download([draftHolding.security.ticker], '2021-4-15')['Adj Close'][0]
                lotsWithMV = draftHolding.draftTaxLots.annotate(mv=F('units') * closingPrice)
                totalMV = lotsWithMV.aggregate(totalMV=Sum('mv'))
                totalsDict[draftPortfolio.id, draftAccount.id, draftHolding.security.ticker] = (totalUnits, totalMV)

    return totalsDict