import time # Time length of program
import sys # Save game details to file
import random
import matplotlib.pyplot as plt
import numpy as np
from player import *
from card import *
from functions import *



if __name__ == "__main__":
    timeStart = time.time()
# ----- Start Simulation of Gameplay -----
    nGames = 100
    nTurns = 100
    fileName = "tests/games" + str(nGames) + "turns" + str(nTurns) + ".txt"
    sys.stdout = open(fileName, "w")

    # Prepare Game
    players = []
    numPlayers = 4
    board = loadBoard()
    chanceDeck, communityDeck = loadCards()
    # Shuffle 3 times to simulate typical shuffling in game prep
    random.shuffle(chanceDeck)
    random.shuffle(communityDeck)
    random.shuffle(chanceDeck)
    random.shuffle(communityDeck)
    random.shuffle(chanceDeck)
    random.shuffle(communityDeck)
    players = createPlayers(numPlayers)

    visitSimulations(players,board,communityDeck,chanceDeck,nTurns,nGames)

    totalDoubles = 0
    print()
    for p in players:
        print(f'{p.name} Money: {p.money}')
        totalDoubles += p.numDoubles

    totalVisits = board['visits'].sum()
    
    print(f'\nTotal Visits: {totalVisits}')
    print(f'Total Doubles: {totalDoubles}')

    board['visitPercent'] = round(board['visits'] / board['visits'].sum() * 100, 2)
    results = board[['name', 'visits','visitPercent']]
    print("\n=== Results Breakdown ===")
    print(results)

    print("\n=== Results By Color/Type ===")
    groups = board.groupby("monopoly",as_index=False)[['monopoly','visits','visitPercent']].sum()
    print(groups)

# ----- End Simulation -----
    totalTime = time.time() - timeStart
    minutes, seconds = divmod(totalTime, 60)
    print(f'\nThis program took {int(minutes)} minutes and {round(seconds,4)} seconds to run.\n')
    sys.stdout.close()

# ------- Graphs ----------
    fig = plt.figure()
    colors = ['brown','deepskyblue','orangered','darkblue','green','gray', 'lightblue', 'rosybrown', 'orange', 'pink', 'black','red', 'crimson','goldenrod', 'yellow']
    types = groups['monopoly'].tolist()
    visitPercents = groups['visitPercent'].tolist()
    y_pos = np.arange(15)
    plt.title('Visit Pct by Color/Types')
    plt.ylabel('Percent')
    plt.xticks(y_pos, types, rotation=90)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)
    plt.bar(types,visitPercents, color=colors, align='center')
    plt.tight_layout()
    plt.show()

    fig = plt.figure()
    colors = ['brown','deepskyblue','orangered','darkblue','green','gray', 'lightblue', 'rosybrown', 'orange', 'pink', 'black','red', 'crimson','goldenrod', 'yellow']
    types = groups['monopoly'].tolist()
    visitPercents = groups['visits'].tolist()
    y_pos = np.arange(60)
    plt.title('Total Visits by Color/Types')
    plt.ylabel('Total Visits')
    plt.xticks(y_pos, types, rotation=90)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.7)
    plt.bar(types,visitPercents, color=colors, align='center')
    plt.tight_layout()
    plt.show()
    