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


def getShares(method="HIFO", targetShares=2, holding=Holding.objects.get(security=Security.objects.get(ticker="AMC"), account=Account.objects.first())):
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

def get():
    return null