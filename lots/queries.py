from django.db.models import Sum, F, Value, DecimalField, ExpressionWrapper, CharField
from .models import *

def summaryTotals(proposalID):
    summaryTotals = Security.objects.prefetch_related('relatedDraftHoldings__draftAccount__draftPortfolio__proposal')
    summaryTotals = summaryTotals.filter(
        relatedDraftHoldings__draftAccount__draftPortfolio__proposal = proposalID
        )
    return summaryTotals

def proposalLots(proposalID):
    # proposalLots = DraftTaxLot.objects.filter(draftHolding__draftAccount__draftPortfolio__proposal_id=proposalID).select_related('referencedLot').prefetch_related('draftHolding__draftAccount__draftPortfolio')
    proposalLots = DraftTaxLot.objects.filter(draftHolding__draftAccount__draftPortfolio__proposal_id=proposalID).select_related('referencedLot').prefetch_related('draftHolding__draftAccount__draftPortfolio')
    return proposalLots
    