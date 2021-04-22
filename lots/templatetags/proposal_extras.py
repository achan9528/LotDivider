from django.db.models import Sum, F
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
def getUnitsFromDraftLot(lot, draftAccount):
    print(lot.draftTaxLotsRelated.get(draftHolding__draftAccount = draftAccount).units)
    return lot.draftTaxLotsRelated.get(draftHolding__draftAccount = draftAccount).units