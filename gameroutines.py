import os
from classes import *

def newGameRoutine() -> tuple[str, list]:
    player_names = []
    players = []
    save_path = "./saves/"
    ans = input("Enter a name for the new save:")

    while(True):
        try:
            os.mkdir(save_path+ans)
        except FileExistsError:
            print("A game with that name already exists!")
            ans = input("Enter a name for the new save:")
            continue
        break
    save_path += ans
    save_path += '/'

    while(True):
        ans = input("How many players are there? ")
        if(ans.isdigit()):
            if(int(ans) > 6 or int(ans) < 1):
                print("Maximum 6 players!")
                continue
            break
        print("That's not a number!")
    player_count = int(ans)
    
    for i in range(player_count):
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        name = input(f"Enter the {ordinal(i+1)} player's name:")
        player_names.append(name)
        players.append(Player(name))

    with open(save_path+"gameinfo.txt", 'w') as f:
        for player in players:
            f.write(f'player {player.name} {player.id.hex}\n')

    save_game_routine(save_path, players, 0)

    return save_path, players


def load_game_routine() -> tuple[str, list, int] :
    players = []
    save_path = ""
    games = []

    for(_, dir_names, _) in os.walk("./saves/"):
        games.extend(dir_names)
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
    save_path += "./saves/" + games[int(ans)-1] + "/"

    with open(save_path+"gameinfo.txt", 'r') as f:
        for line in f:
            words = line.split()
            if(words[0] == "player"):
                players.append(Player(words[1], id=words[2]))

    with open(save_path+"gamestate.txt", 'r') as f:
        gameTime = int(f.readline())
        for line in f:
            words = line.split()
            if(len(words) == 1):
                cur_player = next(x for x in players if x.id.hex == words[0])
                continue
            elif(len(words) == 2):
                match words[0]:
                    case 'blood':
                        cur_player.blood = int(words[1])
                    case 'bloodLoss':
                        cur_player.bloodLoss = int(words[1])
                    case 'pneuma':
                        cur_player.pneuma = int(words[1])
                    case 'pdr':
                        cur_player.pdr = int(words[1])
                    case 'stamina':
                        cur_player.stamina = int(words[1])
                    case 'tiredLvl':
                        cur_player.tiredLvl = int(words[1])
                    case 'hungerPts':
                        cur_player.hungerPts = int(words[1])
                    case _:
                        raise NameError(f'Unrecognized word during loading: {words[0]}')

    return save_path, players, gameTime

def save_game_routine(save_path, players, game_time) -> None:
    with open(save_path+"gamestate.txt", 'w') as f:
        f.write(str(game_time)+'\n')
        for player in players:
            f.write(f'{player.id.hex}\n')
            f.write(player.printState())

    for player in players:
        with open(save_path+player.id.hex+'.txt', 'w') as f:    # Player inventories ###
            f.write('carrying\n')
