from .models import *
from decimal import Decimal
from collections import deque
import pandas as pd

def lots(ticker, accountID, number, cusip, units, date, totalFed, totalState):
    holdingID = createHolding(ticker, accountID)
    createTaxLot(number, ticker, cusip, units, date, totalFed, totalState, holdingID)

def uploadPortfolio(file, portfolioName, accountName):
    portfolioID = createPortfolio(portfolioName, 1)
    accountID = createAccount(accountName, portfolioID)
    df = pd.read_excel(file)
    df.fillna("missing", inplace=True)
    print(df)
    df.apply(lambda x: lots(x['Ticker'], accountID,x['Tax Lot Number'], x['CUSIP'], x['Units'], x['Date Acquired'], x['Total Federal Cost'], x['Total State Cost']), axis=1)

def createPortfolio(name, ownerID):
    if len(Portfolio.objects.filter(name=name)) == 0:
        newPortfolio = Portfolio.objects.create(
            name=name,
            owner=User.objects.get(id=ownerID)
        )
        return newPortfolio.id
    else:
        portfolio = Portfolio.objects.get(
            name=name,
            owner=User.objects.get(id=ownerID)
        )
        return portfolio.id

def createAccount(name, portfolioID):
    if len(Account.objects.filter(name=name,portfolio=Portfolio.objects.get(id=portfolioID))) == 0:
        newAccount = Account.objects.create(
            name=name,
            portfolio=Portfolio.objects.get(id=portfolioID)
        )
        return newAccount.id
    else:
        account = Account.objects.get(
            name=name,
            portfolio=Portfolio.objects.get(id=portfolioID)
        )
        return account.id

def createHolding(ticker, accountID):
    if len(Holding.objects.filter(security=Security.objects.get(ticker=ticker),account=Account.objects.get(id=accountID))) == 0:
        newHolding = Holding.objects.create(
            security=Security.objects.get(ticker=ticker),
            account=Account.objects.get(id=accountID),
        )
        return newHolding.id
    else:
        holding = Holding.objects.get(
            security=Security.objects.get(ticker=ticker),
            account=Account.objects.get(id=accountID),
        )
        return holding.id

def createTaxLot(number, ticker, cusip, units, date, totalFed, totalState, holdingID):
    if number == "missing":
        TaxLot.objects.create(
            units=units,
            totalFederalCost=totalFed,
            totalStateCost=totalState,
            holding=Holding.objects.get(id=holdingID),
        )
    else: 
        if len(TaxLot.objects.filter(number=number, holding=Holding.objects.get(id=holdingID))) == 0:
            TaxLot.objects.create(
                number=number,
                units=units,
                totalFederalCost=totalFed,
                totalStateCost=totalState,
                holding=Holding.objects.get(id=holdingID),
            )

def readExcel(file):
    df = pd.read_excel(file)
    print(df)


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

def splitPortfolio(projectID, accountID, method, numberOfPortfolios, holdingsDict):
    # create new dictionaries which will represent each draft portfolio/account
    # put them into a queue so that way you know which order to put extra shares
    # into
    usedLots = {}
    remainingLots = {}
    portfolios = []
    
    for i in range(int(numberOfPortfolios)):
        portfolios.append({})

        # portfolios.append(
        #     DraftPortfolio.objects.create()
        # )

    portfolioQueue = deque(portfolios)

    for ticker, targetShares in holdingsDict.items():
        tempDict = getLots(
            targetShares=targetShares,
            holding= Holding.objects.get(security=Security.objects.get(ticker=ticker), account=Account.objects.get(id=accountID)),
            method="HIFO"
        )

        usedLots[ticker] = tempDict['usedLots']
        remainingLots[ticker] = tempDict['remainingLots']

        for p in portfolioQueue:
            p[ticker] = {
                'totalCost': 0,
                'totalShares': 0,
            }

        remainderShares = 0
        for lot in tempDict['usedLots']:
            currentLotKey = lot['number']
            for p in portfolioQueue:
                p[ticker][currentLotKey] = 0
            sharesToDistribute = lot['units']

            while sharesToDistribute > 0:

                currentPortfolio = portfolioQueue.pop()

                if remainderShares > 0 and remainderShares <= sharesToDistribute:
                    currentPortfolio[ticker][currentLotKey] += remainderShares
                    currentPortfolio[ticker]['totalShares'] += remainderShares
                    sharesToDistribute -= remainderShares
                    remainderShares -= remainderShares
                    portfolioQueue.appendleft(currentPortfolio)
                elif remainderShares > 0 and remainderShares > sharesToDistribute:
                    currentPortfolio[ticker][currentLotKey] += sharesToDistribute
                    currentPortfolio[ticker]['totalShares'] += sharesToDistribute
                    remainderShares -= sharesToDistribute
                    sharesToDistribute -= sharesToDistribute
                    portfolioQueue.append(currentPortfolio)
                elif sharesToDistribute > 1:
                    currentPortfolio[ticker][currentLotKey] += 1
                    currentPortfolio[ticker]['totalShares'] += 1
                    sharesToDistribute -= 1
                    portfolioQueue.appendleft(currentPortfolio)
                else:
                    currentPortfolio[ticker][currentLotKey] += sharesToDistribute
                    currentPortfolio[ticker]['totalShares'] += sharesToDistribute
                    remainderShares = 1-sharesToDistribute
                    sharesToDistribute -= sharesToDistribute
                    portfolioQueue.append(currentPortfolio)

        portfolioQueue.clear()
        portfolioQueue = deque(portfolios)
    
    proposal = Proposal.objects.create(project=Project.objects.get(id=projectID))
    for portfolio in portfolioQueue:
        draftPortfolio = DraftPortfolio.objects.create(
            proposal = proposal,
        )
        draftAccount = DraftAccount.objects.create(
            draftPortfolio = draftPortfolio,
        )
        for ticker in portfolio.keys():
            draftHolding = DraftHolding.objects.create(
                    security = Security.objects.get(ticker=ticker),
                    draftAccount = draftAccount
                )
            for lot, shares in portfolio[ticker].items():
                if lot != 'totalCost' and lot != 'totalShares':
                    DraftTaxLot.objects.create(
                        number = lot,
                        units = shares,
                        draftHolding = draftHolding,
                    )

    # print(portfolioQueue)
    proposal.name = "Proposal " + str(proposal.id)
    proposal.save()
    return proposal

def getLots(targetShares, holding, method="HIFO"):
    currentLots = []
    currentShares = 0
    returnLots = []
    targetShares = Decimal(targetShares)

    for lot in holding.taxLots.all():
        currentLots.append({
            "number": lot.number,
            "cps": lot.totalFederalCost / lot.units,
            "units": lot.units,
            "acqDate": lot.acquisitionDate,
        })
    
    if method=="HIFO":
        currentLots.sort(key=lambda x: x["cps"])
    elif method=="LIFO":
        currentLots.sort(key=lambda x: x["acqDate"])

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

    return {
        "usedLots": returnLots,
        "remainingLots": currentLots
    }