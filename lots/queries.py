from django.db.models import Sum, F, Value, FloatField
from .models import *

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
                draftLots = draftHolding.draftTaxLots.annotate(cps=F("referencedLot__totalFederalCost")/F("referencedLot__units"),
                unitsAvailable=F("referencedLot__units"), totalFederalCost=F("referencedLot__totalFederalCost"))
                
                returnDict[draftPortfolio, draftAccount].append(draftLots)
    return returnDict

def getDraftTotals(proposal):
    totalsDict = {}

    for draftPortfolio in proposal.draftPortfolios.all():
        for draftAccount in draftPortfolio.draftAccounts.all():
            for draftHolding in draftAccount.draftHoldings.all():
                totalUnits = draftHolding.draftTaxLots.aggregate(totalUnits=Sum('units'))
                totalsDict[draftPortfolio.id, draftAccount.id, draftHolding.security.ticker] = totalUnits

    return totalsDict