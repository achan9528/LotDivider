from django.db.models import Sum, F
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
            for draftHolding in draftAccount.draftHoldings.all():
                referencedLot = draftHolding.draftTaxLots.first().number
                referencedHolding = TaxLot.objects.get(number=referencedLot).holding.id
                annotatedSet = Holding.objects.get(id=referencedHolding).taxLots.annotate(cps=F("totalFederalCost")/F("units"))

                returnDict[draftPortfolio.id, draftAccount.id, draftHolding.security.ticker] = annotatedSet
    return returnDict

def getDraftTotals(proposal):
    totalsDict = {}

    for draftPortfolio in proposal.draftPortfolios.all():
        for draftAccount in draftPortfolio.draftAccounts.all():
            for draftHolding in draftAccount.draftHoldings.all():
                totalUnits = draftHolding.draftTaxLots.aggregate(totalUnits=Sum('units'))
                totalsDict[draftPortfolio.id, draftAccount.id, draftHolding.security.ticker] = totalUnits

    return totalsDict