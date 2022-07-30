import os
from classes import *

def newGameRoutine() -> tuple[str, list]:
    playerNames = []
    players = []
    savePath = "./saves/"
    ans = input("Enter a name for the new save:")

    while(True):
        try:
            os.mkdir(savePath+ans)
        except FileExistsError:
            print("A game with that name already exists!")
            ans = input("Enter a name for the new save:")
            continue
        break
    savePath += ans
    savePath += '/'

    while(True):
        ans = input("How many players are there? ")
        if(ans.isdigit()):
            if(int(ans) > 6 or int(ans) < 1):
                print("Maximum 6 players!")
                continue
            break
        print("That's not a number!")
    playerCount = int(ans)
    
    for i in range(playerCount):
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        name = input(f"Enter the {ordinal(i+1)} player's name:")
        playerNames.append(name)
        players.append(Player(name))

    with open(savePath+"gameinfo.txt", 'w') as f:
        for player in players:
            f.write(f'player {player.name} {player.id.hex}\n')

    saveGameRoutine(savePath, players, 0)

    return savePath, players


def loadGameRoutine() -> tuple[str, list, int] :
    players = []
    savePath = ""
    games = []

    for(_, dirNames, _) in os.walk("./saves/"):
        games.extend(dirNames)
        break

    if(not games):
        print("There are no saved games!")
        return None, []

    print("Choose a game to load from the list below:")
    for i, game in enumerate(games):
        print(f'{i+1} - {game}')

    while(True):
        ans = input()
        if(ans.isdigit()):
            if(int(ans) > len(games) or int(ans) < 1):
                print("That's not an option!")
                continue
            break
        print("That's not a number!")

    players = []
    savePath += "./saves/" + games[int(ans)-1] + "/"

    with open(savePath+"gameinfo.txt", 'r') as f:
        for line in f:
            words = line.split()
            if(words[0] == "player"):
                players.append(Player(words[1], id=words[2]))

    with open(savePath+"gamestate.txt", 'r') as f:
        gameTime = int(f.readline())
        for line in f:
            words = line.split()
            if(len(words) == 1):
                curPlayer = next(x for x in players if x.id.hex == words[0])
                continue
            elif(len(words) == 2):
                match words[0]:
                    case 'blood':
                        curPlayer.blood = int(words[1])
                    case 'bloodLoss':
                        curPlayer.bloodLoss = int(words[1])
                    case 'pneuma':
                        curPlayer.pneuma = int(words[1])
                    case 'pdr':
                        curPlayer.pdr = int(words[1])
                    case 'stamina':
                        curPlayer.stamina = int(words[1])
                    case 'tiredLvl':
                        curPlayer.tiredLvl = int(words[1])
                    case 'hungerPts':
                        curPlayer.hungerPts = int(words[1])
                    case _:
                        raise NameError(f'Unrecognized word during loading: {words[0]}')

    return savePath, players, gameTime

def saveGameRoutine(savePath, players, gameTime) -> None:
    with open(savePath+"gamestate.txt", 'w') as f:
        f.write(str(gameTime)+'\n')
        for player in players:
            f.write(f'{player.id.hex}\n')
            f.write(player.printState())

    for player in players:
        with open(savePath+player.id.hex+'.txt', 'w') as f:    # Player inventories ###
            f.write('carrying\n')

def startEngine(players, tm) -> TimeEngine:
    eng = TimeEngine(players, tm)
    return eng