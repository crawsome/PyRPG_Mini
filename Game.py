import datetime
import os
import pickle
import random
import time
from sqlite3 import connect
import Armor
import Enemy
import Hero
import Item
import Shield
import Weapon
import dbsetup

suspensemode = 0


# TODO: Rewrite in full OOP, and separate / simplify get rid of spaghetti in Game.py

# adds a little suspense to offset the monotony of text input
def suspense():
    s = '.'
    if suspensemode:
        time.sleep(.1)


# One round of a battle
def battle():
    global ourHero
    global ourEnemy
    print('|--------[ENEMY]--------|')
    ourEnemy.printenemyinfo()
    suspense()
    print('|--------[HERO]---------|')
    ourHero.printheroinfo()
    suspense()
    print('|-------[BATTLE]--------|')
    print('|   [a]tk    [d]ef      | \n|   [r]un    [i]tem     |\n| [h]eal coinflip 100g  |')
    print('|-----------------------|\n')
    nextmove = input('Action?\n')
    # U sed for auto attack
    # nextmove = 'a'
    suspense()
    if ourHero.isalive():
        playerturn(nextmove)
    if ourEnemy.isalive():
        enemyturn()
    if not ourHero.isalive():
        ourHero.isbattling = False
        print('YOU DIED')
        print('Cause of death:\nlvl ' + str(ourEnemy.level) + ' ' + str(ourEnemy.name))
        ourHero.printheroinfodetail()
        quit()
    if not ourEnemy.isalive():
        ourHero.isbattling = False
        ourEnemy.reset()
        hpback = int(ourHero.hp/10)
        print('|-------[VICTORY]-------|')
        print('You gained ' + str(ourEnemy.xp) + ' Exp')
        print('You earned ' + str(ourEnemy.gold) + ' Gold')
        print('You ate his sandwich and gained ' + str(hpback) + ' HP back')
        ourHero.hp += hpback
        if ourHero.hp > ourHero.maxhp:
            ourHero.hp = ourHero.maxhp
        if suspensemode:
            input('Press Enter to Continue\n')
            suspense()
        ourHero.xp += ourEnemy.xp
        ourHero.gold += ourEnemy.gold
        if ourHero.xp >= ourHero.nextlevel:
            levelup()
    if not ourHero.isbattling:
        return


def playerturn(m):
    global ourHero
    global ourEnemy
    ourHero.defn = ourHero.basedef + ourarmor.basedefn + ourshield.basedefn
    crit = 0
    critchance = random.randrange(0, 20)
    if critchance == 0:
        crit = ourHero.atk * .4
    effatk = int(ourHero.atk + crit - ourEnemy.defn * .4)
    if effatk < 0:
        effatk = 0
    if m == 'a' or m == '':
        print('|-----[HERO ATTACK]-----|')
        suspense()
        if critchance == 0:
            print('CRITICAL HIT!')
        ourEnemy.hp = ourEnemy.hp - effatk
        ourweapon.dur -= int(effatk * .1)
        if ourEnemy.hp < 0:
            ourEnemy.hp = 0
            ourHero.isbattling = False
        print(str(ourHero.name) + ' attacks Enemy for ' + str(effatk) + ' damage!')
        ourEnemy.printenemyinfo()
    elif m == 'd':
        print('|-------[DEFENSE]-------|')
        ourHero.defn += ourHero.defn * .5
    elif m == 'r':
        print('|-----[RUN ATTEMPT]-----|')
        rand = random.randrange(0, 4)
        if rand == 0:
            print('you ran away')
            ourHero.isbattling = False
            return
        else:
            print('you can\'t run!')
    elif m == 'i':
        pass
    elif m == 'h':
        print('|--------[HEAL]---------|')
        print('Death appears to flip a coin with you.')
        if ourHero.gold >= 100:
            ourHero.gold -= 100
            newrand = random.randrange(0, 1)
            if newrand == 0:
                ourHero.hp = ourHero.maxhp
                print('HEAL SUCCESS\n' + str(ourHero.hp) + '\n')
            else:
                print('HEAL FAILED\nYou lost the roll!\n')

        else:
            print('\nHEAL FAILED\nYou don\'t have enough money!\n')
    if suspensemode:
        input('Press Enter to Continue\n')


def enemyturn():
    global ourHero
    global ourEnemy
    global ourarmor
    global ourshield
    overunder = random.randrange(0, 20)
    suspense()
    if ourEnemy.isalive:
        if overunder == 0:
            ourEnemy.atk += ourEnemy.atk * .2
            print(str(ourEnemy.name) + ' got Angrier!')
            if suspensemode:
                input('Press Enter to Continue\n')
        elif overunder == 1:
            ourEnemy.atk -= ourEnemy.atk * .2
            print(str(ourEnemy.name) + ' got Weaker!')
            if suspensemode:
                input('Press Enter to Continue\n')
        elif overunder == 2:
            print(str(ourEnemy.name) + ' ran away!')
            ourEnemy.hp = 0
            ourHero.isbattling = False
            if suspensemode:
                input('Press Enter to Continue\n')
            return
        if overunder in range(3, ourHero.dodge):
            print('\n|----[ENEMY ATTACK]-----|')
            suspense()
            print(str(ourEnemy.name) + ' swings and misses!')
            print('\n|----[END TURN]---------|\n')
            if suspensemode:
                input('Press Enter to Continue\n')
            return
            suspense()
        if ourHero.isbattling:
            print('\n|----[ENEMY ATTACK]-----|')
            suspense()
            effatk = int(ourEnemy.atk - (.5 * ourHero.defn))
            if effatk < 0:
                effatk = 0
            print('\n' + str(ourEnemy.name) + ' attacks ' + str(ourHero.name) + ' for ' + str(effatk) + ' damage!')
            ourarmor.dur -= int(effatk * .2)
            ourshield.dur -= int(effatk * .2)
            ourHero.hp = ourHero.hp - effatk
            print('\n|----[END TURN]---------|\n')

            if suspensemode:
                input('Press Enter to Continue\n')
            suspense()
            suspense()


def getenemy():
    conn.execute('SELECT * FROM enemies WHERE level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_enemy = random.choice(rows)

    # create random enemy name
    adjectives1 = random.choice((rows[0][1], rows[1][1], rows[2][1], rows[3][1], rows[4][1]))
    adjectives2 = random.choice((rows[0][2], rows[1][2], rows[2][2], rows[3][2], rows[4][2]))
    adjectives3 = random.choice((rows[0][3], rows[1][3], rows[2][3], rows[3][3], rows[4][3]))
    ournewenemy = Enemy.Enemy(new_enemy[0], adjectives1, adjectives2, adjectives3, new_enemy[4], new_enemy[5],
                              new_enemy[6], new_enemy[7], new_enemy[8], new_enemy[9])
    return ournewenemy


# TODO: make levelup and newhero the same function
# TODO: fix leveluparg to work on every level
def newhero():
    conn.execute('SELECT * FROM levelnotes WHERE level = 1;')
    rows = conn.fetchall()
    print('|-----[CHOOSE CLASS]----|\n')
    print('[w]arrior [m]age [h]unter\n')
    ourclass = input()
    if ourclass == 'w':
        ourclass = 'Warrior'
    elif ourclass == 'm':
        ourclass = 'Mage'
    elif ourclass == 'h':
        ourclass = 'Hunter'
    else:
        print('Please enter a valid selection')
    new_hero_data = rows[0]
    ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2],
                           new_hero_data[3], new_hero_data[4], new_hero_data[5])

    return ournewhero


def levelup():
    global ourHero
    print('LEVEL UP!\n ')
    ourHero.printheroinfodetail()
    ourHero.level += 1
    if ourHero.level > 15:
        print('MAX LEVEL! YOU WIN!\n THANKS FOR PLAYING')
        ourHero.printheroinfodetail()
        quit()
    conn.execute('SELECT * FROM levelnotes WHERE level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_hero_data = rows[0]
    ourHero.maxhp = new_hero_data[1] + ourHero.hpaug
    ourHero.hp = ourHero.maxhp + ourHero.hpaug
    ourHero.atk = new_hero_data[2]
    ourHero.defn = new_hero_data[3] + ourHero.defaug
    ourHero.nextlevel += int(new_hero_data[4] * ourHero.levelupaug)
    ourHero.dodge = new_hero_data[5] + ourHero.dodgeaug
    ourHero.printheroinfodetail()


def newweapon():
    conn.execute('SELECT * FROM weapons WHERE "level" = ? AND "class" = ? ;',
                 (str(ourHero.level), str(ourHero.ourclass),))
    rows = conn.fetchall()
    new_weapon_data = rows[0]
    ournewweapon = Weapon.Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3],
                                 new_weapon_data[4], new_weapon_data[5], new_weapon_data[6])
    return ournewweapon


def newarmor():
    conn.execute('SELECT * FROM armor WHERE "level" = ? AND "class" = ? ;',
                 (str(ourHero.level), str(ourHero.ourclass),))
    rows = conn.fetchall()
    new_armor_data = rows[0]
    ournewarmor = Armor.Armor(new_armor_data[0], new_armor_data[1], new_armor_data[2], new_armor_data[3],
                              new_armor_data[4], new_armor_data[5])
    return ournewarmor


def newshield():
    conn.execute('SELECT * FROM shields WHERE "level" = ? AND "class" = ? ;',
                 (str(ourHero.level), str(ourHero.ourclass),))
    rows = conn.fetchall()
    new_shield_data = rows[0]
    ournewshield = Shield.Shield(new_shield_data[0], new_shield_data[1], new_shield_data[2], new_shield_data[3],
                                 new_shield_data[4], new_shield_data[5])
    return ournewshield


def applyequip():
    ourHero.atk = int(ourHero.baseatk + ourweapon.baseatk)
    ourHero.defn = int(ourHero.basedef + ourarmor.defn + ourshield.defn)


def newitem():
    conn.execute('SELECT * FROM items WHERE "grade" = ? ;', ('minor',))
    rows = conn.fetchall()
    new_item_data = rows[0]
    ournewitem = Item.Item(new_item_data[0], new_item_data[1], new_item_data[2], new_item_data[3])
    return ournewitem


def blacksmith():
    global ourweapon
    global ourarmor
    global ourshield
    pass


# show one item, one
def store():
    global ourweapon
    global ourarmor
    global ourshield
    global ouritem
    pass


def camp():
    global ourHero
    ourHero.printheroinfo()
    print('|--------[CAMP]---------|')
    print('| [r]est [i]tem [e]quip |')
    print('| [h]ero    [a]dventure |')
    print('| [p]eddler [b]lacksmith|')
    print('| [l]oad [s]ave [q]uit  |')
    print('|-----------------------|')
    m = input()
    if m == 'r':
        print('|-------[RESTING]-------|')
        ourHero.hp = ourHero.maxhp
        ourHero.printheroinfo()
        return
    elif m == 'i':
        print('|--------[ITEMS]--------|')
        return
    elif m == 'e':
        print('|------[INVENTORY]------|')
        inventory_management()
    elif m == 'h':
        print('|-----[HERO DETAIL]-----|')
        ourHero.printheroinfodetail()
        ourweapon.printweaponinfo()
        ourshield.printshieldinfo()
        ourarmor.printarmorinfo()
    elif m == 'a':
        print('|------[ADVENTURE]------|')
        adventure()
    elif m == 'l':
        print('|------[LOADGAME]-------|')
        loadgame()
    elif m == 's':
        print('|------[SAVEGAME]-------|')
        savegame()
    elif m == 'b':
        print('|-----[BLACKSMITH]------|')
        print(' An old Blacksmith rests at your camp.\nHe shows his wares and services:')
        nextdecision = input('  [f]ix gear\n  [b]uy gear\n')
        if nextdecision == 'f':
            # offer equipment repair for any of the 3 slots, for 1g/durability point
            print('The Blacksmith can offer\nrepair services for 1g/repair point')
            print('Here is your gear durability:\n')
            print('Slot|\tName\t\t|\tDur\t\t|\tBroken?')
            print(str(1) + '\t|\t' + str(ourshield.name) + '\t\t|\t\t' + str(ourshield.dur) + '/' + str(ourshield.maxdur) + '\t|\t' + str(ourshield.isbroken()))
            print(str(2) + '\t|\t' + str(ourweapon.name) + '\t\t|\t\t' + str(ourweapon.dur) + '/' + str(ourweapon.maxdur) + '\t|\t' + str(ourweapon.isbroken()))
            print(str(3) + '\t|\t' + str(ourarmor.name) + '\t\t|\t\t' + str(ourarmor.dur) + '/' + str(ourarmor.maxdur) + '\t|\t' + str(ourarmor.isbroken()))
            decision = input('Which piece of gear do you want to repair?')
            if decision == '1':
                repaircost = ourshield.maxdur - ourshield.dur
                print('Repair Your shield? Cost:' + str(repaircost) + ' gold')
                decision = input('[y]es [n]o')
                if decision == 'y' and ourHero.gold >= repaircost:
                    ourHero.gold -= repaircost
                    ourshield.dur = ourshield.maxdur
                    print('Repair Success.')
            elif decision == '2':
                repaircost = ourweapon.maxdur - ourweapon.dur
                print('Repair Your weapon? Cost:' + str(repaircost) + ' gold')
                decision = input('[y]es [n]o')
                if decision == 'y' and ourHero.gold >= repaircost:
                    ourHero.gold -= repaircost
                    ourweapon.dur = ourweapon.maxdur
                    print('Repair Success.')
            elif decision == '3':
                repaircost = ourarmor.maxdur - ourarmor.dur
                print('Repair Your armor? Cost:' + str(repaircost) + ' gold')
                decision = input('[y]es [n]o')
                if decision == 'y' and ourHero.gold >= repaircost:
                    ourHero.gold -= repaircost
                    ourarmor.dur = ourarmor.maxdur
                    print('Repair Success.')
        if nextdecision == 'b':
            # offer random choice of weapon, armor, or shield at 1.5x value price
            pass
        else:
            print('You walk back to camp')
    elif m == 'p':
        print('|--[PEDDLER\'S WARES]---|')
        print('An old Peddler rests at your camp.\nHe shows his wares:')
        nextdecision = input()
    elif m == 'q':
        print('|--------[QUIT]---------|')
        decision = input('Are you sure?')
        if decision == 'y':
            quit()


# pickle out to hero obj
def loadgame():
    global ourHero
    global ourweapon
    global ourshield
    global ourarmor
    global ouritem
    # load hero object from pickle file
    dirlist = os.listdir('./saves/')
    for i, item in enumerate(dirlist):
        print(str(i) + ' - ' + str(item))
        print(str(datetime.datetime.fromtimestamp(os.path.getmtime('./saves/' + item))))
        print('\n')
    index = input("Which Character?\nOr [c]ancel")
    if index == 'c':
        return
    index = int(index)
    ourpickle = open(('./saves/' + str(dirlist[index])), "rb")
    ourdata = pickle.load(ourpickle)
    ourHero = ourdata[0]
    ourweapon = ourdata[1]
    ourshield = ourdata[2]
    ourarmor = ourdata[3]
    ouritem = ourdata[4]
    # assign this hero object to be the object
    # start the game loop with the loaded hero


# pickle in to hero obj and start gameloop
def savegame():
    global ourHero
    global ourweapon
    global ourshield
    global ourarmor
    global ouritem
    # pickle hero object to file
    # should prompt to overwrite
    heroname = input('Name your save file\nOr [c]ancel')
    if heroname == 'c':
        return
    savefolder = "./saves/"
    filepath = savefolder + heroname + '.hero'
    gamedata = [ourHero, ourweapon, ourshield, ourarmor, ouritem]
    if not os.path.isfile(filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(gamedata, f, -1)
    else:
        answer = input('Overwrite?')
        if answer.lower() == 'y':
            os.remove(filepath)
            print(os.listdir('./saves/'))
            with open(filepath, 'wb') as f:
                pickle.dump(gamedata, f, -1)
        elif answer.lower() == 'n':
            newname = input('Enter New Save file name')
            with open(filepath + str(newname), 'wb') as f:
                pickle.dump(gamedata, f, -1)


# TODO: DOESN'T WORK
def inventory_management():
    for i, item in enumerate(ourHero.items):
        print(str(i) + ' - ' + str(item))
    pass


def gameloop():
    while True:
        adventure()


def adventure():
    global ourEnemy
    global ourHero
    global ourweapon
    global ourshield
    global ouritem
    global ourarmor
    print('|------[ADVENTURE]------|\n')
    print('[a]dventure or [c]amp')
    m = input()
    ourrand = random.randint(0, 100)
    suspense()
    if m == 'a' or m == '':
        if ourrand <= 75:
            ourHero.isbattling = True
            # Make new enemy
            ourEnemy = getenemy()
            print('|[BATTLE]---------------|\n')
            # battle until one is dead
            turnnum = 1
            while ourHero.isalive() and ourEnemy.isalive() and ourHero.isbattling:
                print('|----[TURN ' + str(turnnum) + ']-----------|\n')
                battle()
                turnnum += 1
        elif 75 < ourrand <= 95:
            print('You found and equipped a ')
            itemrand = random.randrange(0, 3)
            if itemrand == 0:
                ourarmor = newarmor()
                ourarmor.printarmorinfo()
                ourHero.items.append(ourarmor)
            elif itemrand == 1:
                ourweapon = newweapon()
                ourweapon.printweaponinfo()
                ourHero.items.append(ourweapon)
            elif itemrand == 2:
                ourshield = newshield()
                ourshield.printshieldinfo()
                ourHero.items.append(ourshield)
            elif itemrand == 3:
                ouritem = newitem()
                ouritem.printiteminfo()
                ourHero.items.append(ouritem)
            applyequip()
        elif 95 < ourrand <= 100:
            print('You find a traveler,')
            print('He says:')
            suspense()
            with open('./quoteslist.txt', 'rb') as f:
                quotelist = f.read().splitlines()
                quote = random.choice(quotelist)
                quote = quote.decode('utf-8')
                print(quote)
            suspense()
            print('\nYou venture back to camp')
            pass
    elif m == 'c':
        camp()

    def healingpotion(effect):
        global ourHero
        global ouritem
        ourHero.hp += effect
        if ourHero.hp > ourHero.maxhp:
            ourHero.hp = ourHero.maxhp
            ourHero.items.remove('')
        pass

    def explosivemanavial(self, effect):
        global ourHero
        global ouritem
        pass

    def healthregenpotion(self, effect):
        global ourHero
        global ouritem
        pass

    def hastepotion(self, effect):
        global ourHero
        global ouritem
        pass

    def weaponrepairtincture(self, effect):
        global ourHero
        global ouritem
        pass


if __name__ == '__main__':
    # this is for repopulating the database with modified CSV files
    # TODO: Make so database will not append if run more than once
    # Create all game databases (only needs to run once to make databases)
    print('Reload database?')
    foo = input('[y]es [n]o')
    if foo == 'y':
        dbsetup.setup()

    print('=========================\n'
          '|        MiniRPG        |\n'
          '=========================')

    # our database path
    dbpath = './db/game.db'

    # import and create our player database
    gamedb = connect(dbpath)
    conn = gamedb.cursor()

    # Make new global hero and enemy which will change over time
    ourHero = newhero()

    # Make a basic weapon
    ourweapon = newweapon()

    # Make a basic armor
    ourarmor = newarmor()

    # Make a basic shield
    ourshield = newshield()

    # Make a potion
    ouritem = newitem()

    # apply out equipped items stats
    applyequip()

    # make a basic enemy object
    ourEnemy = getenemy()

    ourHero.name = input('Please enter your name, ' + str(ourHero.ourclass) + '\n')

    ourHero.heroperks()

    gameloop()
