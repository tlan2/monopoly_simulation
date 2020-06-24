# Game Actions
import pandas as pd
import random
from card import *
from player import *

def loadBoard():
    """ Loads board in a dataframe """

    board = pd.read_csv("board.csv")
    board['visits'] = 0
    board['owned'] = False
    return board

def loadCards():
    """ Loads Chance & Community Chest card info """

    chanceDeck = []
    communityDeck = []
    chance = pd.read_csv("chance.csv", engine='python')
    chest = pd.read_csv("communityChest.csv", engine='python')

    for i in range(chance.shape[0]):
        card = Card(chance,i)
        chanceDeck.append(card)
    
    for i in range(chest.shape[0]):
        card = Card(chest,i)
        communityDeck.append(card)

    return chanceDeck, communityDeck

def createPlayers(n):
    """ Create n players for game """

    players = []
    for i in range(1,n+1):
        pName = 'p' + str(i)
        p = Player(pName)
        players.append(p)

    return players

def visitSimulations(players, board, communityCards, chanceCards, nTurns, nGames):
    """ Performs simulations on object """
    for i in range(1,nGames+1):
        print(f'\n=== Game #{i} ===')
        for t in range(1, nTurns + 1):
            for p in players:
                print(f'\n=== {p.name} Turn #: {t} ===')
                rollDice(p,players,board,communityCards,chanceCards)
    
    return

def jailStrategy(p, board):
    """ Applies jail rules and strategy """

    payJailThreshold = 200
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    totalRoll = d1 + d2
    doubles = (d1 == d2)
    previousLocation = p.location
    jailFee = 50


    print(f'Jail Rolls: {p.jailRolls}')

    # Use Get out of Jail Free card
    if(p.jailFreeCard):
        print("Used \"Get Out of Jail Free\" card.")
        p.jail = False
        p.jailRolls = 0
        p.location += totalRoll
        board.loc[p.location,"visits"] += 1
        print(f'd1 = {d1} | d2 = {d2}')
        print(f'totalRoll = {totalRoll}')
        print(f'Prev: {previousLocation} | New: {p.location}')
        prevName = board.loc[previousLocation,'name']
        newName = board.loc[p.location,'name']
        print(f'{prevName} | {newName} ')
        return p
    # On 3rd Jail Roll
    elif(p.jailRolls == 3):
        print("Final Free Jail Roll.")
        if(doubles):
            p.jail = False
            p.jailRolls = 0
            p.location += totalRoll
            board.loc[p.location,"visits"] += 1
            p.numDoubles += 1
            print(f'd1 = {d1} | d2 = {d2}')
            print(f'totalRoll = {totalRoll}')
            print(f'Prev: {previousLocation} | New: {p.location}')
            prevName = board.loc[previousLocation,'name']
            newName = board.loc[p.location,'name']
            print(f'{prevName} | {newName} ')
            return p
        else:
            print("No Doubles on 3rd Jail Row. Pay $50 fee.")
            if(p.canPay(jailFee)):
                p.money -= 50
                p.jail = False
                p.jailRolls = 0
                p.location += totalRoll
                board.loc[p.location,"visits"] += 1
                print(f'd1 = {d1} | d2 = {d2}')
                print(f'totalRoll = {totalRoll}')
                print(f'Prev: {previousLocation} | New: {p.location}')
                prevName = board.loc[previousLocation,'name']
                newName = board.loc[p.location,'name']
                print(f'{prevName} | {newName} ')
                return p
            # else:
            #     print(f"Game Over for {p.name}.")
            #     p.inGame = False
            #     return p
    elif(p.money <= payJailThreshold):
        if(doubles):
            print("JAIL - Rolled doubles! Free from Jail!")
            p.jail = False
            p.jailRolls = 0
            p.numDoubles += 1
            p.location += totalRoll
            board.loc[p.location,"visits"] += 1
            print(f'd1 = {d1} | d2 = {d2}')
            print(f'totalRoll = {totalRoll}')
            print(f'Prev: {previousLocation} | New: {p.location}')
            prevName = board.loc[previousLocation,'name']
            newName = board.loc[p.location,'name']
            print(f'{prevName} | {newName} ')
        else:
            print("JAIL - No doubles. Turn over.")
            board.loc[p.location,"visits"] += 1
            return p
    else:
        print(f"{p.name} paid Jail Fee of $50.")
        p.money -= jailFee
        print(p.money)
        p.jail = False
        p.jailRolls = 0
        p.location += totalRoll
        board.loc[p.location,"visits"] += 1
        print(f'd1 = {d1} | d2 = {d2}')
        print(f'totalRoll = {totalRoll}')
        print(f'Prev: {previousLocation} | New: {p.location}')
        prevName = board.loc[previousLocation,'name']
        newName = board.loc[p.location,'name']
        print(f'{prevName} | {newName} ')
        return p

def rollDice(p, playerList, board, communityCards, chanceCards):
        """ 
            Method to simulate 3 rolling outcomes. 
            1. Two different dice = Perform action & turn over
            2. Same dice & total # of rolls < 3 = Perform action & roll Again
            3. Same dice & total # of rolls is 3 = Go to Jail
        """

        rollCount = 1
        doubles = True
        jail = 10

        # Apply Jail Rules
        if(p.jail):
            p.jailRolls += 1
            p = jailStrategy(p, board)
            return
        
        while(doubles):
            # 3 straight doubles --> Go to Jail!
            if(rollCount == 3):
                print("Roll 3 straight doubles. Go directly to jail!")
                p.numDoubles += 1
                p.location = jail
                p.jail = True
                board.loc[p.location,"visits"] += 1
                return

            d1 = random.randint(1,6)
            d2 = random.randint(1,6)
        
            totalRoll = d1 + d2
            previousLocation = p.location
            newLocation = previousLocation + totalRoll
            
            # If pass Go!, collect 200
            if (newLocation >= 40):
                p.money += 200
                p.location = newLocation % 40
                board.loc[p.location,"visits"] += 1
                # Only Possible Community Chest Space near Go
                if(p.location == 2):
                    print('Community Chest Loc-2')
                    p = communityChest(p, playerList, board, communityCards)
                    print(f'After CC p.location = {p.location}')
                    # if(p.location-2 != 0):
                    #     board.loc[p.location,"visits"] += 1
                # Only Possible Chance Space near Go
                elif(p.location == 7):
                    print('Chance Loc-7')
                    p = chance(p, playerList, board, chanceCards)
                    print(f'new p.location = {p.location}')
                    # if(p.location-7 != 0):
                    #      board.loc[p.location,"visits"] += 1
            else:
                # All non-Chance & non-Community Chest Spaces
                p.location = previousLocation + totalRoll
                board.loc[p.location,"visits"] += 1
                if(p.location == 30):
                    p.location = jail
                    p.jail = True
                    board.loc[p.location,"visits"] += 1
                    print(f'd1 = {d1} | d2 = {d2}')
                    print(f'totalRoll = {totalRoll}')
                    print(f'Prev: {previousLocation} | New: {p.location}')
                    prevName = board.loc[previousLocation,'name']
                    newName = board.loc[p.location,'name']
                    print(f'{prevName} | {newName} ')
                    return
                # Community Chest Spaces
                elif(p.location == 2 or p.location == 17 or p.location == 33):
                    print(f'Community Chest Loc-{p.location}')
                    p=communityChest(p, playerList, board, communityCards)
                    print(f'After CC p.location = {p.location}')
                    # if(p.location-2 != 0 or p.location-17 != 0 or p.location-33 != 0):
                    #      board.loc[p.location,"visits"] += 1
                # Chance Spaces
                elif(p.location == 7 or p.location == 22 or p.location == 36):
                    print(f'Chance Loc-{p.location}')
                    p=chance(p, playerList, board, chanceCards)
                    print(f'After Chance p.location = {p.location}')
                    # if(p.location- 7 != 0 or p.location-22 != 0 or p.location-36 != 0):
                    #      board.loc[p.location,"visits"] += 1

            print(f'd1 = {d1} | d2 = {d2}')
            print(f'totalRoll = {totalRoll}')
            print(f'Prev: {previousLocation} | New: {p.location}')
            prevName = board.loc[previousLocation,'name']
            newName = board.loc[p.location,'name']
            print(f'{prevName} | {newName} ')

           # Rolled Doubles
            if(d1 == d2):
                print("You rolled doubles! Go again!\n")
                doubles == True
                p.numDoubles += 1
                rollCount += 1
                continue
            else:
                # End of Turn
                print("Turn Over.")
                doubles = False
                return

def communityChest(p, playerList, board, cards):
    """ Simulates pulling a community chess card in game """

    otherPlayers = [player for player in playerList if player.name != p.name]
   
    card = cards.pop(0)
    print(card.text)

    if(card.category == 'money'):
        p.money += int(card.action)

    elif(card.category == 'moneyPlayers'):
        # Receive $10/$50 from other players
        total = 0
        for player in otherPlayers:
            player.money -= int(card.action)
            total += int(card.action)
        p.money += total
    
    elif(card.category == 'move'):
        # Go To Jail card
        if(card.id == 5):
            p.jail = True
            p.location = int(card.action)
        # Move to Go
        else:
            p.location = int(card.action)

    # elif(card.category == 'moneyHouses'):
    #     # Pay tax for houses and hotels card
    
    elif(card.category == 'keep'):
        # Get Out of Jail Free card
        p.jailFreeCard = True

    cards.append(card)

    return p
    
def chance(p, playerList, board, cards):
    """ Simulates pulling a community chess card in game """

    otherPlayers = [player for player in playerList if player.name != p.name]
    
    card = cards.pop(0)
    cid = card.id
    print(card.text)

    if(card.category == 'move'):
        # Move back 3 spaces
        if(cid == 8):
            p.location = p.location-3
        # Go to Jail
        elif(cid == 9):
            p.location = int(card.action)
            p.jail = True
        # Advanced to Boardwalk.
        elif(cid == 13):
            p.location = int(card.action)
    
    elif(card.category == 'money'):
        p.money += int(card.action)

    elif(card.category == 'moveGo'):
        # Advance to Go and Collect $200
        if(cid == 0):
            p.money += 200
            p.location = int(card.action) 
        # Advance to Illinois Avenue
        elif(cid == 1):
            if(p.location >= 24 and p.location <= 39):
                p.money += 200
                p.location = int(card.action)
            else:
                p.location = int(card.action)
        # Advanced to St. Charles Place. Collect $200 if you pass go
        elif(cid == 2):
            if(p.location >= 11 and p.location <= 39):
                p.money += 200
                p.location = int(card.action)
            else:
                p.location = int(card.action)
        # Advance to Reading Railroad. Collect $200 if you pass go
        elif(cid == 12):
            if(p.location <= 5):
                p.location = int(card.action)
            else:
                p.money += 200
                p.location = int(card.action)

    elif(card.category == 'moveRailroad'):
        # Move to nearest RR
        # Pennsylvania RR
        if(p.location == 7):
            p.location = 15
        # B&O RR
        elif(p.location == 22):
            p.location = 25
        # Reading RR
        elif(p.location == 36):
            p.location = 5

    elif(card.category == 'moveUtility'):
        # Move to nearest Utility
        # Electric Company
        if(p.location == 7 or p.location == 36):
            p.location = 12
        # Water Works
        else:
            p.location = 28

    # elif(card.category == 'moneyHouses'):
    #     # Pay $25 per house, $115 per hotel
    
    elif(card.category == 'keep'):
        # Get out of Jail Free card
        p.jailFreeCard = True

    elif(card.category == 'moneyPlayers'):
        # Pay each player $50
        totalPay = 0
        for player in otherPlayers:
            player.money += 50
            totalPay += 50
        p.money -= totalPay

    cards.append(card)

    return p

# def propertyAction(location, board):
#     """ Executes action of property """

#     pass
