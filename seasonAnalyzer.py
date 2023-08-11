#Made Aug 10, 2023 by Gregory Post Davis
#Special Thanks to ocarina919 for the foundation
#This was written based off of the ReplayTool seen on my GitHub
#Which was written primarily by ocarina919 with testing and some addtional features by me

import re
from os import listdir
from os import getcwd
from os.path import isfile, join


class Pokemon:
    def __init__(self, mon_name):
        self.name = mon_name
        self.moveList = []
        self.teraTypes = []
        self.timesBrought = 0

    def printPokemon(self):
        print(self.name + ":", self.timesBrought)
        print('\n'+"Moves")
        for moves in self.moveList:
            print("   ", moves)
        print('\n'+"Tera Types")
        for teras in self.teraTypes:
            print("   ", teras)

    def add_unique_move(self, new_move):
        if not any(move1 == new_move for move1 in self.moveList):
            self.moveList.append(new_move)
        else:
            pass

    def add_unique_tera(self, new_tera):
        if not any(tera == new_tera for tera in self.teraTypes):
            self.teraTypes.append(new_tera)
        else:
            pass


class Trainer:
    def __init__(self, mon_name):
        self.name = mon_name
        self.pokemon = []

    def add_unique_pokemon(self, new_pokemon):
        if not any(mon1.name == new_pokemon for mon1 in self.pokemon):
            self.pokemon.append(Pokemon(new_pokemon))
        else:
            pass

    def writeLog(self):
        g = open(self.name+".txt", "w")
        for pokes in self.pokemon:
            g.write(pokes.name + ": " + str(pokes.timesBrought) + '\n' + "   Moves" + '\n')
            for moves in pokes.moveList:
                g.write("       " + moves+'\n')
            if len(pokes.moveList) < 1:
                g.write("       None"+'\n')
            g.write("   Tera Types" + '\n')
            for teras in pokes.teraTypes:
                g.write("       " + teras+'\n')
            if len(pokes.teraTypes) < 1:
                g.write("       None"+'\n')
            g.write("="*20+'\n')
        g.close()


nicknames = dict()
Trainers = []


def nick_to_name(nick, nicknamed):
    for poke in nicknamed.keys():
        if nicknamed[poke] == nick:
            if ',' in poke:
                poke = poke.split(",")[0]
            return poke


def add_unique_trainer(new_trainer):
    if not any(trainer.name == new_trainer.lower() for trainer in Trainers):
        if len(new_trainer.strip()) > 0:
            Trainers.append(Trainer(new_trainer.lower()))
    else:
        pass


#Establish File Path as Current Directory and take all html files
mypath = getcwd()
onlyFiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".html")]
#


for entry in onlyFiles:
    with open(entry, encoding='utf-8') as f:
        file = f.read()

    file = file.split("<script type=\"text/plain\" class=\"battle-log-data\">")[1]
    file = file.split("</script>")[0]
    lines = file.split("\n")

    usernames = []
    players = dict()
    nicks = dict()
    currently_out = dict()

    #Acutal Looping goes in here
    for line in lines:
        result = re.match("^\|(.*?)\|(.*)", line)
        if result:
            prefix = result[1]
            args = result[2].split("|")
        else:
            continue

        if prefix == "player":
            players[args[0]] = args[1]
            usernames.append(args[1])
            add_unique_trainer(args[1].lower())

        elif prefix == "poke":
            postCut = args[1].split(",")
            pkmn = postCut[0]

            if pkmn == "Urshifu-*":
                pkmn = "Urshifu"
            elif pkmn == "Silvally-*":
                pkmn = "Silvally"
            elif pkmn == "Dudunsparce-*":
                pkmn = "Dudunsparce"
            elif pkmn == "Keldeo-*":
                pkmn = "Keldeo"
            elif pkmn == "Zarude-*":
                pkmn = "Zarude"
            elif pkmn.startswith("Tauros"):
                pkmn = "Tauros"
            elif pkmn.startswith("Castform"):
                pkmn = "Castform"
            elif pkmn.startswith("Burmy"):
                pkmn = "Burmy"
            elif pkmn.startswith("Wormadam"):
                pkmn = "Wormadam"
            elif pkmn.startswith("Deoxys"):
                pkmn = "Deoxys"
            elif pkmn.startswith("Unown"):
                pkmn = "Unown"
            elif pkmn.startswith("Cherrim"):
                pkmn = "Cherrim"
            elif pkmn.startswith("Gastrodon"):
                pkmn = "Gastrodon"
            elif pkmn.startswith("Arceus"):
                pkmn = "Arceus"
            elif pkmn.startswith("Basculin"):
                pkmn = "Basculin"
            elif pkmn.startswith("Deerling"):
                pkmn = "Deerling"
            elif pkmn.startswith("Sawsbuck"):
                pkmn = "Sawsbuck"
            elif pkmn.startswith("Meloetta"):
                pkmn = "Meloetta"
            elif pkmn.startswith("Genesect"):
                pkmn = "Genesect"
            elif pkmn.startswith("Vivillon"):
                pkmn = "Vivillon"
            elif pkmn.startswith("Flabebe"):
                pkmn = "Flabebe"
            elif pkmn.startswith("Floette"):
                pkmn = "Floette"
            elif pkmn.startswith("Florges"):
                pkmn = "Florges"
            elif pkmn.startswith("Minior"):
                pkmn = "Minior"



            for trainer in Trainers:
                if trainer.name.lower() == players.get(args[0]).lower():
                    trainer.add_unique_pokemon(pkmn)
                    for mon in trainer.pokemon:
                        if mon.name == pkmn:
                            mon.timesBrought = mon.timesBrought + 1
                        pass
            pass

        elif prefix == "switch" or prefix == "drag":

            nicks[args[1]] = args[0]
            player_id = args[0].split(":")[0]
            currently_out[player_id] = args[0]
            #(currently_out.get(player_id))

        elif prefix == "move":
            user = args[0]
            move = args[1]
            if nick_to_name(user, nicks):
                user = nick_to_name(user, nicks)

            if args[0].startswith("p1"):
                attacker = players.get("p1").lower()
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_move(move)
            else:
                attacker = players.get("p2").lower()
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_move(move)
            pass

        elif prefix == "-terastallize":
            tera_type = args[1]
            user = args[0]

            if nick_to_name(user, nicks):
                user = nick_to_name(user, nicks)

            if args[0].startswith("p1"):
                attacker = players.get("p1").lower()
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_tera(tera_type)
            else:
                attacker = players.get("p2").lower()
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_tera(tera_type)
            pass

    ####################
    # End of HTML File #
    ####################

#########################
# End of Gathering Data #
#########################
for coach in Trainers:
    coach.writeLog()
