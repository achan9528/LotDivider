from django.db.models import Sum, F, Value, DecimalField, ExpressionWrapper, CharField
from .models import *


def summarizeProposal(proposal):
    summaryDict = {
        'lots': getDraftLotCPS(proposal),
        # 'totals': getDraftTotals(proposal),
    }
    # print(summaryDict)
    return summaryDict

def getDraftLotCPS(proposal):    
    returnDict = {}

    for draftPortfolio in proposal.draftPortfolios.all():
        for draftAccount in draftPortfolio.draftAccounts.all():
            returnDict[draftPortfolio, draftAccount] = []
            for draftHolding in draftAccount.draftHoldings.all():
                draftLots = draftHolding.draftTaxLots.annotate(
                    cps=ExpressionWrapper(
                        (F("referencedLot__totalFederalCost") * 1.0) / (F("referencedLot__units") * 1.0),
                        output_field=DecimalField(decimal_places=4)),
                    unitsAvailable=F("referencedLot__units"), 
                    totalFederalCost=F("referencedLot__totalFederalCost"))
                returnDict[draftPortfolio, draftAccount].append(draftLots)
    return returnDict


def test(proposalID):
    allLotsInProposal = list(DraftTaxLot.objects.filter(
        draftHolding__draftAccount__draftPortfolio__proposal = proposalID
        ).values_list('referencedLot',flat=True).distinct())

    mergedTable = TaxLot.objects.prefetch_related('draftTaxLotsRelated').filter(pk__in=allLotsInProposal)
    
    test = Security.objects.prefetch_related('relatedDraftHoldings__draftAccount__draftPortfolio__proposal')
    test = test.filter(
        relatedDraftHoldings__draftAccount__draftPortfolio__proposal = proposalID
        )
    

    return mergedTable
