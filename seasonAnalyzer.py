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

    def usedPokemon(self):
        self.timesBrought = self.timesBrought + 1

    def add_unique_move(self, new_move):
        if not any(move1 == new_move for move1 in self.moveList):
            self.moveList.append(new_move)
            print("added", new_move, "for", self.name)
            for x in self.moveList:
                print(x)
        else:
            print("did not add", new_move, "for", self.name)
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

    def printName(self):
        print(self.name)

    def add_unique_pokemon(self, new_pokemon):
        if not any(mon1.name == new_pokemon for mon1 in self.pokemon):
            self.pokemon.append(Pokemon(new_pokemon))
            print(new_pokemon, "added")
        else:
            print(new_pokemon, "not added")
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


def nick_to_name(nick, nicknamed):
    for poke in nicknamed.keys():
        if nicknamed[poke] == nick:
            if ',' in poke:
                poke = poke.split(",")[0]
            return poke


nicknames = dict()
Trainers = []


def add_unique_trainer(new_trainer):
    if not any(trainer1.name == new_trainer for trainer1 in Trainers):
        if len(new_trainer.strip()) > 0:
            Trainers.append(Trainer(new_trainer))
            #print("new trainer added")
    else:
        #print("no trainer added")
        pass


mypath = getcwd()
onlyFiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".html")]


# for entry in onlyFiles:
#     print(entry)
# print("="*10)


for entry in onlyFiles:
    with open(entry, encoding='utf-8') as f:
        file = f.read()
    print("="*10, entry, "="*10)

    file = file.split("<script type=\"text/plain\" class=\"battle-log-data\">")[1]
    file = file.split("</script>")[0]
    lines = file.split("\n")

    players = dict()
    usernames = []
    nicks = dict()
    last_move = []
    last_source = ""
    turn = 0
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
            add_unique_trainer(args[1])

        elif prefix == "poke":
            postCut = args[1].split(",")
            pkmn = postCut[0]
            #print(postCut[0])

            for trainer in Trainers:
                if trainer.name == players.get(args[0]):
                    #print(players.get(args[0]))
                    trainer.add_unique_pokemon(pkmn)
                    for mon in trainer.pokemon:
                        if mon.name == pkmn:
                            print(mon.name, mon.timesBrought)
                            mon.timesBrought = mon.timesBrought + 1
                        pass
                # for p in x.pokemon:
                #     print(p.name)
                # print("="*20)

        elif prefix == "switch" or prefix == "drag":

            nicks[args[1]] = args[0]
            player_id = args[0].split(":")[0]
            currently_out[player_id] = args[0]
            #(currently_out.get(player_id))

        elif prefix == "move":
            target = args[2]
            move = args[1]
            user = args[0]

            if nick_to_name(user, nicks):
                user = nick_to_name(user, nicks)
            if nick_to_name(target, nicks):
                target = nick_to_name(target, nicks)

            #print("*-"*30, user)

            if args[0].startswith("p1"):
                attacker = players.get("p1")
                print(players.get("p1"))
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_move(move)
            else:
                attacker = players.get("p2")
                print(players.get("p2"))
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_move(move)

        elif prefix == "-terastallize":
            tera_type = args[1]
            user = args[0]

            if nick_to_name(user, nicks):
                user = nick_to_name(user, nicks)

            if args[0].startswith("p1"):
                attacker = players.get("p1")
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_tera(tera_type)
            else:
                attacker = players.get("p2")
                for trainer in Trainers:
                    if trainer.name == attacker:
                        for mons in trainer.pokemon:
                            if mons.name == user:
                                mons.add_unique_tera(tera_type)

    ##############
    #End of File #
    ##############

#############
#End of Gathering Data
for coach in Trainers:
    coach.writeLog()

    #print(coach.name, len(coach.pokemon))
    # for mons in coach.pokemon:
    #     mons.printPokemon()
    #print("="*10)
