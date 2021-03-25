from .models import *
from decimal import Decimal

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

def splitPortfolio(accountID, method, numberOfPortfolios, holdingsDict):
    
    usedLots = {}
    remainingLots = {}

    for ticker, targetShares in holdingsDict.items():
        tempDict = getLots(
            targetShares=targetShares,
            holding= Holding.objects.get(security=Security.objects.get(ticker=ticker), account=Account.objects.get(id=accountID))
        )

        # debugging and print check
        # print(ticker + "used lots:")
        # print(returnDict["usedLots"])
        # print("\n")

        # print(ticker + "remaining lots:")
        # print(returnDict["remainingLots"])
        # print("\n")
        
        usedLots[ticker] = tempDict[usedLots]
        remainingLots[ticker] = tempDict[remainingLots]
    

    return returnDict

def getLots(method, targetShares, holding):
    # restrictions when you are splitting positions
    # you cannot simply deplete lots and then switch to the
    # next recipient because you wouldn't be passing on the gains
    # from the shares in the most equitable way. You need to
    # 1) ensure that there are no fractional positions left (fractional lots are ok)
    # 2) ensure that the gains are split evenly amongst other individuals

    currentLots = []
    currentShares = 0
    returnLots = []
    targetShares = Decimal(targetShares)

    for lot in holding.taxLots.all():
        currentLots.append({
            "number": lot.number,
            "cps": lot.totalFederalCost / lot.units,
            "units": lot.units
        })
    
    currentLots.sort(key=lambda x: x["cps"])
    # print(currentLots)
    # print("\n")
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

    # print(returnLots)
    # print("\n")
    # print(currentLots)

    return {
        "usedLots": returnLots,
        "remainingLots": currentLots
    }

def get():
    # select portfolio
    # select account
    # select holdings
    # select how many portfolios you want to split it into
    # select the optional stuff (HIFO, etc.)
    # getShares function which chooses shares based off of the
        # selections
    # split the shares into the different portfolios
    # save the portfolios as drafts

    return null