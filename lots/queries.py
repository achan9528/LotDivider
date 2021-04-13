from django.db.models import Sum
from .models import *

def summarizeProposal(proposal):
    # for all lots in each holiding in each portfolio in 
    # the portfolio, find the total shares and total MV
    # of the shares. Save this total to a dictionary
    unitTotals = {}

    for draftPortfolio in proposal.draftPortfolios.all():
        for draftAccount in draftPortfolio.draftAccounts.all():
            totalsDictionary = {}
            for holding in draftAccount.draftHoldings.all():
                totalUnits = holding.draftTaxLots.aggregate(totalUnits=Sum('units'))
                totalsDictionary[holding.security.ticker] = totalUnits
            
            unitTotals[draftPortfolio.id] = totalsDictionary

    return unitTotals    