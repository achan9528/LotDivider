from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django import template
from datetime import date
import yfinance as yf

register = template.Library()

@register.filter
def getType(something):
    print(type(something))
    return(type(something))

@register.filter
def tmvLabel(title):
    today = date.today().strftime("%Y-%m-%d")
    return f"Total Market Value as of {today}"

@register.filter
def getTotalUnits(setOfLots):
    return list(setOfLots.aggregate(
        totalUnits=Sum('units')
        ).values())[0]

@register.filter
def getTotalAvailableUnits(setOfLots):
    return list(setOfLots.aggregate(
        totalUnits=Sum('unitsAvailable')
        ).values())[0]

@register.filter
def getTotalMV(setOfLots):
    today = date.today().strftime("%Y-%m-%d")
    closingPrice = yf.download(
        [setOfLots.first().referencedLot.holding.security.ticker],
        today)['Adj Close'][0]
    setOfLots = setOfLots.annotate(mv=F('units') * closingPrice)
    return list(setOfLots.aggregate(totalMV=Sum('mv')).values())[0]

@register.filter
def getDraftPortfolioTotalMV(allLotSets):
    today = date.today().strftime("%Y-%m-%d")
    totalMV = 0
    tickers = []
    for s in allLotSets:
        tickers.append(
            s.first().referencedLot.holding.security.ticker
        )
    
    closingPrices = yf.download(tickers, today)['Adj Close']
    print(closingPrices)
    for s in allLotSets:
        annotatedSet = s.annotate(
            mv = F('units') * closingPrices[s.first().referencedLot.holding.security.ticker][0]
        )
        totalMV += list(annotatedSet.aggregate(Sum('mv')).values())[0]
    return totalMV

@register.filter
def getUnitsFromDraftLot(draftPortfolio):
    return lot.draftTaxLotsRelated.get(draftHolding__draftAccount = draftAccount).units

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
        ).order_by('-relatedDraftHoldings__draftAccount__draftPortfolio__id').filter(ticker=ticker)

    context = {
        'ticker': ticker,
        'summaryTotals': totals,
        'proposal': proposal,
        'proposalLots': proposalLots,
    }
    return context

@register.inclusion_tag('proposalTableColumn.html')
def proposalTableColumn(lot, draftPortfolio):
    context = {
        'draftTaxLot': lot.draftTaxLotsRelated.get(draftHolding__draftAccount__draftPortfolio=draftPortfolio)
    }
    return context