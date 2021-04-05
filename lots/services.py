from .models import *
from decimal import Decimal
from collections import deque

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
            holding= Holding.objects.get(security=Security.objects.get(ticker=ticker), account=Account.objects.get(id=accountID))
        )

        # debugging and print check
        print(ticker + "used lots:")
        print(tempDict["usedLots"])
        print("\n")

        # print(ticker + "remaining lots:")
        # print(returnDict["remainingLots"])
        # print("\n")
        
        usedLots[ticker] = tempDict['usedLots']
        remainingLots[ticker] = tempDict['remainingLots']

        # you need to know how many portfolios to split
        # the lots into and how many target shares you are
        # dealing with. This is an issue because if you have
        # an odd number of shares splitting into an even
        # number of portfolios, then you are going to be left
        # with a fractional amount of shares on the 
        # receiving portfolios which is not allowed. How
        # do you determine who gets the extra share? For
        # now, we will evenly distribute the extra shares
        # so that there is a trade off. Later implmentations
        # will be such that you can designate someone to have
        # all of the extra shares

        # if the target shares divided by the number of 
        # portfolios is a whole number, then you know that
        # you can simply divide each lot by the number of 
        # portfolios you have


        # for each lot in usedLots, distribute amongst the
        # queue
        

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
            # print(sharesToDistribute)
            # if the lot has less shares than the number
            # of portfolios
            # if lot.units < numberOfPortfolios:

                # determine how many shares can be distributed
                # amongst the portfolios
                # if there are 3 accounts and only 2 shares
                # in the lot, then you will have to determine
                # that the first two accounts in the queue
                # will receive the shares.
            while sharesToDistribute > 0:
                # choose which account will receive the
                # shares in the lot based on the queue
                currentPortfolio = portfolioQueue.pop()
                # print(currentPortfolio[ticker])
                if remainderShares > 0:
                    currentPortfolio[ticker][currentLotKey] += remainderShares
                    currentPortfolio[ticker]['totalShares'] += remainderShares
                    sharesToDistribute -= remainderShares
                    remainderShares -= remainderShares
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

        # for p in portfolioQueue:
        #     print("Portfolio")
        #     print(p)
        # print(portfolioQueue)
        portfolioQueue.clear()
        portfolioQueue = deque(portfolios)
        # Case 1: If the number of shares is less than
        # the number of portfolios

        # if targetShares < numberOfPortfolios:

        # use a queue to determine who gets what shares

            #Case a: if the target shares is odd and the # of 
            # portfolios is even

                # if targetShares % 2 != 0 and 
                # numberOfPortfolios % 2 == 0:

                    # round the shares down to the nearest even number
                    # and then evenly distribute amongst the portfolios.

                    # tempTarget = math.floor(targetShares)
                    # remainingShares = targetShares - tempTarget

                    # for each lot you will be using, if the 
                    # lot is evenly divisible, then you can 

            #Case b: if the target shares is even and you're
            # dividing it amongst an odd number of portfolios

            # case c: if the target shares is odd and you're
            # dividing it amongst and odd number of portfolios

            #Case d: if the target shares is even and you're
            # dividing it amongst an even number of portfolios
        
        # Case #2: if the target shares is greater than 
        # or equal to the the number of portflios

            #Case a: if the target shares is odd and the # of 
            # portfolios is even

            # round the shares down to the nearest even number
            # and then evenly distribute amongst the portfolios.

            #Case b: if the target shares is even and you're
            # dividing it amongst an odd number of portfolios

            # case c: if the target shares is odd and you're
            # dividing it amongst and odd number of portfolios

            #Case d: if the target shares is even and you're
            # dividing it amongst an even number of portfolios
    
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
    return proposal

def getLots(targetShares, holding, method="HIFO"):
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