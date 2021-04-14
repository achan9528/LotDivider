from django.db.models import Sum, F
from .models import *

def summarizeProposal(proposal):
    # for all lots in each holiding in each portfolio in 
    # the portfolio, find the total shares and total MV
    # of the shares. Save this total to a dictionary
    unitTotals = {}

    for draftPortfolio in proposal.draftPortfolios.all():
        for draftAccount in draftPortfolio.draftAccounts.all():
            totalsDictionary = {}
            for draftHolding in draftAccount.draftHoldings.all():
                referencedLot = draftHolding.draftTaxLots.first().number
                referencedHolding = TaxLot.objects.get(number=referencedLot).holding.id
                annotatedSet = Holding.objects.get(id=referencedHolding).taxLots.annotate(cps=F("totalFederalCost")/F("units"))

                totalUnits = draftHolding.draftTaxLots.aggregate(totalUnits=Sum('units'))
                totalsDictionary[draftHolding.security.ticker] = totalUnits
            unitTotals[draftPortfolio.id] = totalsDictionary

    return unitTotals    