from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When
from django import template
from datetime import date
import yfinance as yf

register = template.Library()

@register.filter
def getType(something):
    print(type(something))
    return(type(something))

@register.filter
def monetize(amount):
    print(type(amount))
    if type(amount)==None:
        amount=0
    return f"${amount}"

@register.inclusion_tag('proposalTable.html')
def proposalTable(proposal, summaryTotals, proposalLots):
    d = date.today().strftime("%Y-%m-%d")
    tickers = list(summaryTotals.values_list('ticker', flat=True).distinct())
    closingPrices = yf.download(tickers, d)['Adj Close']

    context = {
        'proposal': proposal,
        'summaryTotals': summaryTotals,
        'tickers': tickers,
        'closingPrices': closingPrices,
        'closingDate': d,
        'proposalLots': proposalLots
    }
    return context

@register.inclusion_tag('proposalTableRow.html')
def proposalTableRow(summaryTotals, ticker, closingPrices, closingDate, proposal, proposalLots):
    totals = summaryTotals.filter(ticker=ticker).annotate(mv=F('relatedDraftHoldings__draftTaxLots__units')*closingPrices[ticker][0])
    totals = totals.values('relatedDraftHoldings__draftAccount__draftPortfolio').annotate(
        totalMV=Sum('mv'),
        totalUnits=Sum('relatedDraftHoldings__draftTaxLots__units')
        )
    lots = list(
        proposalLots.filter(
            draftHolding__security__ticker=ticker, 
            draftHolding__draftAccount__draftPortfolio__proposal=proposal
            ).values_list('referencedLot__number', flat=True).distinct()
        )
    proposalLots = proposalLots.filter(referencedLot__number__in=lots)\
        .annotate(
            cps=ExpressionWrapper(
                    F('referencedLot__totalFederalCost')/F('referencedLot__units'),
                    output_field=DecimalField(decimal_places=2)
                ), 
            mv=ExpressionWrapper(
                F('units')*closingPrices[ticker][0], 
                    output_field=DecimalField(decimal_places=2)
                )
        )
    context = {
        'ticker': ticker,
        'summaryTotals': totals,
        'proposal': proposal,
        'proposalLots': proposalLots,
        'lots': lots,
    }
    return context

@register.inclusion_tag('proposalTableColumn.html')
def proposalTableColumn(lot, draftPortfolio, proposalLots):
    context = {
        'draftTaxLot': proposalLots.get(referencedLot__number=lot,draftHolding__draftAccount__draftPortfolio=draftPortfolio)
    }
    return context