from django.db.models import Sum, F, Value, DecimalField, ExpressionWrapper, CharField
from .models import *

def summaryTotals(proposalID):
    summaryTotals = Security.objects.prefetch_related('relatedDraftHoldings__draftAccount__draftPortfolio__proposal')
    summaryTotals = summaryTotals.filter(
        relatedDraftHoldings__draftAccount__draftPortfolio__proposal = proposalID
        )
    return summaryTotals

def proposalLots(proposalID):
    proposalLots = TaxLot.objects.prefetch_related('draftTaxLotsRelated').filter(draftTaxLotsRelated__draftHolding__draftAccount__draftPortfolio__proposal_id = proposalID)
    return proposalLots
    