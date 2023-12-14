# Made Aug 10, 2023 by Gregory Post Davis
# Special Thanks to ocarina919 for the foundation
# This was written based off of the ReplayTool seen on my GitHub
# Which was written primarily by ocarina919 with testing and some addtional features by me

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
        print('\n' + "Moves")
        for moves in self.moveList:
            print("   ", moves)
        print('\n' + "Tera Types")
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
    def __init__(self, t_name):
        self.name = t_name
        self.pokemon = []
        self.wins = 0
        self.losses = 0
        self.gp = 0

    def add_unique_pokemon(self, new_pokemon):
        if not any(mon1.name == new_pokemon for mon1 in self.pokemon):
            self.pokemon.append(Pokemon(new_pokemon))
        else:
            pass

    def writeLog(self):
        self.losses = self.gp - self.wins
        g = open(self.name + ".txt", "w")
        g.write(self.name + ": " + str(self.wins) + "-" + str(self.losses) + '\n')
        for pokes in self.pokemon:
            g.write(pokes.name + ": " + str(pokes.timesBrought) + '\n' + "   Moves" + '\n')
            for moves in pokes.moveList:
                g.write("       " + moves + '\n')
            if len(pokes.moveList) < 1:
                g.write("       None" + '\n')
            g.write("   Tera Types" + '\n')
            for teras in pokes.teraTypes:
                g.write("       " + teras + '\n')
            if len(pokes.teraTypes) < 1:
                g.write("       None" + '\n')
            g.write("=" * 20 + '\n')
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
    t = re.sub('[^0-9a-zA-Z]+', '', new_trainer).lower()
    if not any(tr.name == t for tr in Trainers):
        if len(t) > 0:
            Trainers.append(Trainer(t))
            print("New Trainer:", t)
    else:
        pass

def handle_formes(pkmn):
    if pkmn.startswith("Tauros"):
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
    elif pkmn.startswith("Zarude"):
        pkmn = "Zarude"
    elif pkmn.startswith("Urshifu"):
        pkmn = "Urshifu"
    elif pkmn.startswith("Silvally"):
        pkmn = "Silvally"
    elif pkmn.startswith("Dudunsparce"):
        pkmn = "Dudunsparce"
    elif pkmn.startswith("Keldeo"):
        pkmn = "Keldeo"
    elif pkmn.startswith("Pikachu"):
        pkmn = "Pikachu"
    elif pkmn.startswith("Greninja"):
        pkmn = "Greninja"

    return pkmn

# Establish File Path as Current Directory and take all html files
mypath = getcwd()
onlyFiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".html")]
#


for entry in onlyFiles:
    playersAdded = 0
    with open(entry, encoding='utf-8') as f:
        file = f.read()

    file = file.split("<script type=\"text/plain\" class=\"battle-log-data\">")[1]
    file = file.split("</script>")[0]
    lines = file.split("\n")

    usernames = []
    players = dict()
    nicks = dict()
    currently_out = dict()

    # Acutal Looping goes in here
    for line in lines:
        result = re.match("^\|(.*?)\|(.*)", line)
        if result:
            prefix = result[1]
            args = result[2].split("|")
        else:
            continue

        if prefix == "player":
            if playersAdded < 2:
                #players is an array of the two players in the game
                players[args[0]] = re.sub('[^0-9a-zA-Z]+', '', args[1]).lower()
                usernames.append(re.sub('[^0-9a-zA-Z]+', '', args[1]).lower())
                add_unique_trainer(re.sub('[^0-9a-zA-Z]+', '', args[1]).lower())

                print(args[1].lower())
                for t in Trainers:
                    if t.name == re.sub('[^0-9a-zA-Z]+', '', args[1]).lower():
                        t.gp = t.gp + 1
                playersAdded = playersAdded + 1

        elif prefix == "poke":
            postCut = args[1].split(",")
            pkmn = handle_formes(postCut[0])

            for trainer in Trainers:
                unmodified_name = players.get(args[0])
                simple_name = re.sub('[^0-9a-zA-Z]+', '', unmodified_name).lower()
                if trainer.name == simple_name:
                    trainer.add_unique_pokemon(pkmn)
                    for mon in trainer.pokemon:
                        if mon.name == pkmn:
                            mon.timesBrought = mon.timesBrought + 1
                        pass
            pass

        elif prefix == "switch" or prefix == "drag":
            pkmn_nickname = args[1]
            pkmn_name = handle_formes(args[0])

            nicks[pkmn_nickname] = pkmn_name
            player_id = args[0].split(":")[0]
            currently_out[player_id] = args[0]
            # (currently_out.get(player_id))

        elif prefix == "move":
            user = args[0]
            move = args[1]
            if nick_to_name(user, nicks):
                user = handle_formes(nick_to_name(user, nicks))

            if len(args) > 3:
                if "Metronome" in args[3] or "Assist" in args[3]:
                    break

            if args[0].startswith("p1"):
                attacker = re.sub('[^0-9a-zA-Z]+', '', players.get("p1")).lower()
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_move(move)
            else:
                attacker = re.sub('[^0-9a-zA-Z]+', '', players.get("p2")).lower()
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
                user = handle_formes(nick_to_name(user, nicks))

            if args[0].startswith("p1"):
                attacker = re.sub('[^0-9a-zA-Z]+', '', players.get("p1").lower())
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_tera(tera_type)
            else:
                attacker = re.sub('[^0-9a-zA-Z]+', '', players.get("p2").lower())
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_tera(tera_type)

        elif prefix == "win":
            for t in Trainers:
                if t.name.lower() == re.sub('[^0-9a-zA-Z]+', '', args[0]).lower():
                    t.wins = t.wins + 1
                    t.losses = t.gp - t.wins
        else:
            pass


    ####################
    # End of HTML File #
    ####################

#########################
# End of Gathering Data #
#########################

for coach in Trainers:
    coach.writeLog()
    # print(coach.name, coach.gp, "Games Played", coach.wins, coach.losses)
