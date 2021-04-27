from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value, Count
from django import template
from datetime import date
import yfinance as yf
from itertools import chain


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
    totals = summaryTotals.filter(ticker=ticker).annotate(
            mv=F('relatedDraftHoldings__draftTaxLots__units')*closingPrices[ticker][0],
            cost=(F('relatedDraftHoldings__draftTaxLots__referencedLot__totalFederalCost')/F('relatedDraftHoldings__draftTaxLots__referencedLot__units'))*F('relatedDraftHoldings__draftTaxLots__units')
        )
    totals = totals.values('relatedDraftHoldings__draftAccount__draftPortfolio').annotate(
        totalMV=Sum('mv'),
        totalUnits=Sum('relatedDraftHoldings__draftTaxLots__units'),
        totalCost=Sum('cost')
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

@register.inclusion_tag('proposalTableTotals.html')
def proposalTableTotals(proposalLots, tickers, closingPrices, closingDate, proposal):

    # get all of the unique draftPortfolios in the proposal.
    # store these in a dictionary so that the total MV's can be added
    # looping through each ticker.
    temp = list(proposal.draftPortfolios.all().values_list('id',flat=True).distinct())
    totals = {}
    for p in temp:
        totals[p] = 0

    # loop through each ticker, annotating the queryset filtered for the ticker with 
    # the currentMV
    # add the MV to the portfolio dictionary
    for ticker in tickers:
        qs = proposalLots.filter(draftHolding__security__ticker=ticker)\
            .annotate(mv=F('units')*closingPrices[ticker][0])
        holdingTotals = qs.values('draftHolding__draftAccount__draftPortfolio')\
            .annotate(totalMV=Sum('mv'))
        for holdingTotal in holdingTotals:
            pID = holdingTotal['draftHolding__draftAccount__draftPortfolio']
            total = holdingTotal['totalMV']
            totals[pID] += total

    # return the dictionary as context for the template tag
    context = {
        'totals': totals
    }

    return context

    # # This is the initial method that I wrote to solve this but it does not 
    # # work because the | operator does not correctly append the two querysets together.
    # # It takes the mv of earlier rows and applies to later rows which is incorrect.
    
    # sets = [] # sets to be merged back together

    # # filter the proposalLots so that there are only the ones from the current proposal
    # # proposalLots = proposalLots.filter(draftHolding__draftAccount__draftPortfolio__proposal=proposal)

    # # filter the proposalLots by ticker. Store this in a temp variable
    # # for each ticker, annotate the queryset to include the closingPrice * units = mv
    # # calculate the totalMV for the position for each portfolio and store it in totals
    # # add tempResults to the sets list 
    # for ticker in tickers:
    #     temp = proposalLots.filter(draftHolding__security__ticker=ticker).annotate(mv=F('units')*closingPrices[ticker][0])
    #     sets.append(temp)
    
    # # combine all sets together into one bigSet
    # bigSet = sets[0]
    
    # for i in range(1,len(sets)):
    #     bigSet = bigSet | sets[i]

    # c = sets[0] | sets[1]
    # print(c.values('draftHolding__draftAccount__draftPortfolio', 'draftHolding__security__ticker','mv', 'units'))
    # print(bigSet.filter(referencedLot__number='43874c17-6174-4d7e-91f0-e1575199fb48').values('draftHolding__draftAccount__draftPortfolio', 'draftHolding__security__ticker','mv'))
    
    # # aggregate and return these results in context
    # results = c.values('draftHolding__draftAccount__draftPortfolio').annotate(totalMV=Sum('mv')).order_by()
    # print(results) 
    # context = {
    #     'results': results
    # }
    # print(context)

