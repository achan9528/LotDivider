from .models import *

def getHoldings(accountID):
    holdings = []

    for holding in Account.objects.get(id=accountID).holdings.all():

        totalFederalCost = 0
        totalStateCost = 0
        totalUnits = 0

        for lot in holding.taxLots.all():
            totalFederalCost += lot.totalFederalCost
            totalStateCost += lot.totalFederalCost
            totalUnits += lot.units

        holdings.append({
            "ticker": holding.security.ticker,
            "name": holding.security.name,
            "totalFederalCost": totalFederalCost,
            "totalStateCost": totalStateCost,
            "totalUnits": totalUnits,
        })
    
    return holdings


def getShares(method="HIFO", targetShares=2, holding=Holding.objects.get(security=Security.objects.get(ticker="AMC"))):
    # restrictions when you are splitting positions
    # you cannot simply deplete lots and then switch to the
    # next recipient because you wouldn't be passing on the gains
    # from the shares in the most equitable way. You need to
    # 1) ensure that there are no fractional positions left (fractional lots are ok)
    # 2) ensure that the gains are split evenly amongst other individuals

    currentLots = []
    currentShares = 0
    returnLots = []

    for lot in holding.taxLots.all():
        currentLots.append({
            "number": lot.number,
            "cps": lot.totalFederalCost / lot.units,
            "units": lot.units
        })
    
    currentLots.sort(key=lambda x: x["cps"])
    print(currentLots)
    print("\n")
    while currentShares < targetShares:
        currentLot = currentLots[-1]
        if currentLot["units"] <= targetShares - currentShares:
            currentShares += currentLot["units"]
            temp = currentLots.pop()
            returnLots.append(temp)
        else:
            temp = currentLots.pop()
            temp["units"] = temp["units"] - (targetShares - currentShares)
            returnLots.append({
                "number": temp["number"],
                "cps": temp["cps"],
                "units": targetShares - currentShares
            })
            currentLots.append(temp)
            currentShares = targetShares

    print(returnLots)
    print("\n")
    print(currentLots)
    return [returnLots, currentLots]

# def get():
    # determine how many portfolios you will need
    # to split the portfolio into

    # determine how many shares for each holding you
    # will need

    # determine who will get any extra lots

    # determine which lots you will use

    # split

    # update the portfolio with the remaining share
    # information

# targets = dictionary object which has all of the information
# needed to split the portfolio in the target ones
def divideHoldings(targets):
    # nested dictionaries to build the portfolios, like
    # how I did it in VBA
    # a dictionary within a dictionary so the step before 
    # it is important because it will calculate the shares
    # needed in all portfolios, then you can pass
    # that target dictionary into the function


    # pass the targets in through the forms
    # this is the main function which will call other
    # functions
    return null