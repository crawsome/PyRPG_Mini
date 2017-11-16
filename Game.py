import datetime
import os
import pickle
import random
import time
from sqlite3 import connect
import Enemy
import Hero
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
    global ourhero
    global ourenemy
    ourhero.battlecount += 1
    print('|--------[ENEMY]--------|')
    ourenemy.printenemyinfo()
    suspense()
    print('|--------[HERO]---------|')
    ourhero.printheroinfo()
    suspense()
    print('|-------[BATTLE]--------|')
    print('|   [a]tk    [d]ef      | \n|   [r]un    [i]tem     |\n| [h]eal coinflip 100g  |')
    print('|-----------------------|\n')
    nextmove = input('Action?\n')
    # U sed for auto attack
    # nextmove = 'a'
    suspense()
    if ourhero.isalive():
        playerturn(nextmove)
    if ourenemy.isalive():
        enemyturn()
    if not ourhero.isalive():
        ourhero.isbattling = False
        print('YOU DIED')
        print('Cause of death:\nlvl ' + str(ourenemy.level) + ' ' + str(ourenemy.name))
        ourhero.printheroinfodetail()
        quit()
    if not ourenemy.isalive():
        ourhero.isbattling = False
        ourenemy.reset()
        hpback = int(ourhero.maxhp * .4)
        print('|-------[VICTORY]-------|')
        print('You gained ' + str(ourenemy.xp) + ' Exp')
        print('You earned ' + str(ourenemy.gold) + ' Gold')
        # 20% chance to get some health back.
        if random.randrange(0, 4) == 0:
            print('\nYou found his lunch\n and gained ' + str(hpback) + ' HP back')
            ourhero.hp += hpback
            if ourhero.hp > ourhero.maxhp:
                ourhero.hp = ourhero.maxhp
        if suspensemode:
            input('Press Enter to Continue\n')
            suspense()
        ourhero.xp += ourenemy.xp
        ourhero.gold += ourenemy.gold
        if ourhero.xp >= ourhero.nextlevel:
            ourhero.levelup()
    if not ourhero.isbattling:
        return


def playerturn(m):
    global ourhero
    global ourenemy
    ourhero.defn = ourhero.basedef + ourhero.ourarmor.basedefn + ourhero.ourshield.basedefn
    crit = 0
    critchance = random.randrange(0, 20)
    if critchance == 0:
        crit = ourhero.atk * .4
    effatk = int(ourhero.atk + crit - ourenemy.defn * .35)
    if effatk < 0:
        effatk = 0
    if m == 'a' or m == '':
        print('|-----[HERO ATTACK]-----|')
        suspense()
        if critchance == 0:
            print('CRITICAL HIT!')
        ourenemy.hp = ourenemy.hp - effatk
        ourhero.ourweapon.dur -= int(effatk * .01)
        if ourenemy.hp < 0:
            ourenemy.hp = 0
            ourhero.isbattling = False
        print(str(ourhero.name) + ' attacks Enemy for ' + str(effatk) + ' damage!')
        ourenemy.printenemyinfo()
    elif m == 'd':
        print('|-------[DEFENSE]-------|')
        ourhero.defn += ourhero.defn * .5
    elif m == 'r':
        print('|-----[RUN ATTEMPT]-----|')
        rand = random.randrange(0, 4)
        if rand == 0:
            print('you ran away')
            ourhero.isbattling = False
            return
        else:
            print('you can\'t run!')
    elif m == 'i':
        item_management()
    elif m == 'h':
        print('|--------[HEAL]---------|')
        print('Death appears to flip a coin with you.')
        if ourhero.gold >= 100:
            ourhero.gold -= 100
            newrand = random.randrange(0, 1)
            if newrand == 0:
                ourhero.hp = ourhero.maxhp
                print('HEAL SUCCESS\n' + str(ourhero.hp) + '\n')
            else:
                print('HEAL FAILED\nYou lost the roll!\n')

        else:
            print('\nHEAL FAILED\nYou don\'t have enough money!\n')
    if suspensemode:
        input('Press Enter to Continue\n')

    #accounts for health regen potion
    if ourhero.regentimer > 0:
        regen = int(ourhero.hp * .2)
        print('You regen ' + str(regen) + 'HP')
        ourhero.hp += regen
        ourhero.regentimer -= 1
        if ourhero.hp > ourhero.maxhp:
            ourhero.hp = ourhero.maxhp

    #accounts for haste potion for 5 turn dodge increases
    ourhero.dodge = ourhero.basedodge
    if ourhero.hastetimer > 0:
        ourhero.dodge = ourhero.basedodge + 2
        print('Your dodge chance is elevated')
        ourhero.hastetimer -= 1
    else:
        ourhero.dodge = ourhero.basedodge


def enemyturn():
    global ourhero
    global ourenemy
    overunder = random.randrange(0, 20)
    suspense()
    if ourenemy.isalive:
        if overunder == 0:
            ourenemy.atk += ourenemy.atk * .2
            print(str(ourenemy.name) + ' got Angrier!')
            if suspensemode:
                input('Press Enter to Continue\n')
        elif overunder == 1:
            ourenemy.atk -= ourenemy.atk * .2
            print(str(ourenemy.name) + ' got Weaker!')
            if suspensemode:
                input('Press Enter to Continue\n')
        elif overunder == 2:
            print(str(ourenemy.name) + ' ran away!')
            ourenemy.hp = 0
            ourhero.isbattling = False
            if suspensemode:
                input('Press Enter to Continue\n')
            return
        if overunder in range(3, ourhero.dodge):
            print('\n|----[ENEMY ATTACK]-----|')
            suspense()
            print(str(ourenemy.name) + ' swings and misses!')
            print('\n|----[END TURN]---------|\n')
            if suspensemode:
                input('Press Enter to Continue\n')
            return
            suspense()
        if ourhero.isbattling:
            print('\n|----[ENEMY ATTACK]-----|')
            suspense()
            effatk = int(ourenemy.atk - (.5 * ourhero.defn))
            if effatk < 0:
                effatk = 0
            print('\n' + str(ourenemy.name) + ' attacks ' + str(ourhero.name) + ' for ' + str(effatk) + ' damage!')
            ourhero.ourarmor.dur -= int(effatk * .2)
            ourhero.ourshield.dur -= int(effatk * .2)
            ourhero.hp = ourhero.hp - effatk
            print('\n|----[END TURN]---------|\n')

            if suspensemode:
                input('Press Enter to Continue\n')
            suspense()
            suspense()


def getenemy():
    conn.execute('SELECT * FROM enemies WHERE level = ' + str(ourhero.level) + ';')
    rows = conn.fetchall()
    new_enemy = random.choice(rows)

    # create random enemy name
    adjectives1 = random.choice((rows[0][1], rows[1][1], rows[2][1], rows[3][1], rows[4][1]))
    adjectives2 = random.choice((rows[0][2], rows[1][2], rows[2][2], rows[3][2], rows[4][2]))
    adjectives3 = random.choice((rows[0][3], rows[1][3], rows[2][3], rows[3][3], rows[4][3]))
    ournewenemy = Enemy.Enemy(new_enemy[0], adjectives1, adjectives2, adjectives3, new_enemy[4], new_enemy[5],
                              new_enemy[6], new_enemy[7], new_enemy[8], new_enemy[9])
    return ournewenemy


# TODO: make ourhero.levelup and newhero the same function
# TODO: fix ourhero.leveluparg to work on every level
def newhero():
    conn.execute('SELECT * FROM levelnotes WHERE level = 1;')
    rows = conn.fetchall()
    print('|-----[CHOOSE CLASS]----|\n')
    print('[w]arrior [m]age [h]unter\n')
    ourclass = input()
    if ourclass == 'w' or ourclass == '':
        ourclass = 'warrior'
    elif ourclass == 'm':
        ourclass = 'mage'
    elif ourclass == 'h':
        ourclass = 'hunter'
    else:
        print('Please enter a valid selection')
    new_hero_data = rows[0]
    ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2],
                           new_hero_data[3], new_hero_data[4], new_hero_data[5])
    return ournewhero


def blacksmith():
    global ourhero
    print(' An old Blacksmith rests at your camp.\nHe shows his wares and services:')
    nextdecision = input('  [f]ix gear\n  [b]uy gear\n')
    if nextdecision == 'f':
        # offer equipment repair for any of the 3 slots, for 1g/durability point
        print('The Blacksmith can offer\nrepair services for 1g/repair point')
        print('Here is your gear durability:\n')
        print('Slot|\tName\t\t|\tDur\t\t|\tBroken?')
        print(
            str(1) + '\t|' + str(ourhero.ourshield.name) + ' ' + str(ourhero.ourshield.type) + '\t\t' + str(ourhero.ourshield.dur) + '/' + str(
                ourhero.ourshield.maxdur) + '\t' + str(ourhero.ourshield.isbroken()))
        print(
            str(2) + '\t|' + str(ourhero.ourweapon.name) + ' ' + str(ourhero.ourweapon.type) + '\t\t' + str(ourhero.ourweapon.dur) + '/' + str(
                ourhero.ourweapon.maxdur) + '\t' + str(ourhero.ourweapon.isbroken()))
        print(str(3) + '\t|' + str(ourhero.ourarmor.name) + ' ' + str(ourhero.ourarmor.type) + '\t\t' + str(ourhero.ourarmor.dur) + '/' + str(
            ourhero.ourarmor.maxdur) + '\t' + str(ourhero.ourarmor.isbroken()))
        decision = input('Which piece of gear do you want to repair?\n[a] for all\n')
        if decision == '1' or decision == 'a':
            repaircost = ourhero.ourshield.maxdur - ourhero.ourshield.dur
            print('Repair Your shield?\nCost: ' + str(repaircost) + ' gold')
            decision2 = input('[y]es [n]o\n')
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourshield.dur = ourhero.ourshield.maxdur
                print('Repair Success.')
        if decision == '2' or decision == 'a':
            repaircost = ourhero.ourweapon.maxdur - ourhero.ourweapon.dur
            print('Repair Your weapon?\nCost: ' + str(repaircost) + ' gold')
            decision2 = input('[y]es [n]o\n')
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourweapon.dur = ourhero.ourweapon.maxdur
                print('Repair Success.')
        if decision == '3' or decision == 'a':
            repaircost = ourhero.ourarmor.maxdur - ourhero.ourarmor.dur
            print('Repair Your armor?\nCost: ' + str(repaircost) + ' gold')
            decision2 = input('[y]es [n]o\n')
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourarmor.dur = ourhero.ourarmor.maxdur
                print('Repair Success.')
    if nextdecision == 'b':
        # offer random choice of weapon, armor, or shield at 1.5x value price
        pass
    pass


# show one item, one
def store():
    global ourweapon
    global ourarmor
    global ourshield
    global ouritem
    pass


def camp():
    global ourhero
    ourhero.printheroinfo()
    print('|--------[CAMP]---------|')
    print('| [r]est [i]tem [e]quip |')
    print('| [h]ero    [a]dventure |')
    print('| [p]eddler [b]lacksmith|')
    print('| [l]oad [s]ave [q]uit  |')
    print('|-----------------------|')
    m = input()
    if m == 'r':
        print('|-------[RESTING]-------|')
        ourhero.hp = ourhero.maxhp
        ourhero.printheroinfo()
        return
    elif m == 'i':
        print('|--------[ITEMS]--------|')
        item_management()
        return
    elif m == 'e':
        print('|------[INVENTORY]------|')
        item_management()
    elif m == 'h':
        print('|-----[HERO DETAIL]-----|')
        ourhero.printheroinfodetail()
        ourhero.ourweapon.printweaponinfo()
        ourhero.ourshield.printshieldinfo()
        ourhero.ourarmor.printarmorinfo()
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
        blacksmith()
    elif m == 'p':
        print('|--[PEDDLER\'S WARES]---|')
        print('An old Peddler rests at your camp.\nHe shows his wares:')
        nextdecision = input()
        if nextdecision == 'b':
            # offer random choice of weapon, armor, or shield at 1.5x value price
            pass
    elif m == 'q':
        print('|--------[QUIT]---------|')
        decision = input('Are you sure?')
        if decision == 'y':
            quit()
    else:
        print('You walk back to camp')


# pickle out to hero obj
def loadgame():
    global ourhero
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
    ourhero = ourdata

    # assign this hero object to be the object
    # start the game loop with the loaded hero


# pickle in to hero obj and start gameloop
def savegame():
    global ourhero
    # pickle hero object to file
    # should prompt to overwrite
    heroname = input('Name your save file\nOr [c]ancel')
    if heroname == 'c':
        return
    savefolder = "./saves/"
    filepath = savefolder + heroname + '.hero'
    gamedata = ourhero
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
def item_management():
    global ourhero
    print('|-[CHOOSE ITEM]-|')
    for i, item in enumerate(ourhero.items):
        print(str(i) + ' \tName: ' + str(item.name) + '\tEffect: ' + str(item.effect))
    itemindex = input('Please enter decision')
    if itemindex not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                         '17', '18', '19', '20']:
        print('Please enter a valid choice')
        return
    ourhero.ouritem = ourhero.items[int(itemindex)]
    ourhero.activeitem = ourhero.ouritem
    del(ourhero.items[int(itemindex)])
    print('Using ' + str(ourhero.ouritem.name))
    if ourhero.ouritem.name == 'Healing Potion':
        healingpotion()
    if ourhero.ouritem.name == 'Explosive Mana Vial':
        explosivemanavial()
    if ourhero.ouritem.name == 'Health Regen Potion':
        healthregenpotion()
    if ourhero.ouritem.name == 'Haste Potion':
        hastepotion()
    if ourhero.ouritem.name == 'Weapon Repair Tincture':
        weaponrepairtincture()
    pass


# TODO: DOESN'T WORK
def gear_management():
    global ourshield
    global ourweapon
    global ourarmor
    print(str(1) + ourshield.name + '\n' + str(2) + ourweapon.name + '\n' + str(3) + ourarmor.name + '\n')

    pass


def gameloop():
    while True:
        adventure()


def adventure():
    global ourenemy
    global ourhero
    print('|------[ADVENTURE]------|\n')
    print('[a]dventure or [c]amp')
    m = input()
    ourrand = random.randint(0, 100)
    suspense()
    if m == 'a' or m == '':
        if ourrand <= 75:
            ourhero.isbattling = True
            # Make new enemy
            ourenemy = getenemy()
            print('|[BATTLE]---------------|\n')
            # battle until one is dead
            turnnum = 1
            while ourhero.isalive() and ourenemy.isalive() and ourhero.isbattling:
                print('|----[TURN ' + str(turnnum) + ']-----------|\n')
                battle()
                turnnum += 1
        elif 75 < ourrand <= 95:
            print('You found and equipped')
            itemrand = random.randrange(0, 5)
            if itemrand == 0:
                ourhero.ourarmor = ourhero.newarmor()
                ourhero.ourarmor.printarmorinfo()
            elif itemrand == 1:
                ourhero.ourweapon = ourhero.newweapon()
                ourhero.ourweapon.printweaponinfo()
            elif itemrand == 2:
                ourhero.ourshield = ourhero.newshield()
                ourhero.ourshield.printshieldinfo()
            elif 3 <= itemrand <= 5:
                ourhero.ouritem = ourhero.newitem()
                ourhero.ouritem.printiteminfo()
                ourhero.items.append(ourhero.ouritem)
            ourhero.applyequip()
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

def healingpotion():
    global ourhero
    healed = ourhero.activeitem.effect
    ourhero.hp += healed
    print('You heal for ' + str(healed) + ' HP')
    if ourhero.hp > ourhero.maxhp:
        ourhero.hp = ourhero.maxhp
        ourhero.activeitem = 0
    return

def explosivemanavial():
    global ourhero
    global ourenemy
    dmg = ourhero.activeitem.effect
    ourenemy.hp -= ourhero.activeitem.effect
    print('\nThe Mana Vial EXPLODES!\nDealing ' + str(dmg) + ' damage to\n' + str(ourenemy.name))
    ourhero.activeitem = 0
    return

# adds health per turn
def healthregenpotion():
    global ourhero
    print('5 turns health regen')
    ourhero.regentimer = 5
    ourhero.activeitem = 0
    pass

# two attacks
def hastepotion():
    global ourhero
    print('5 turns dodge buff')
    ourhero.hastetimer = 5
    ourhero.activeitem = 0
    pass

# heals 60% of dur points to weapon
def weaponrepairtincture():
    global ourhero
    rep = ourhero.ourweapon.maxdur * .6
    print('You repaired your weapon for\n' + str(rep) + ' durability points')
    ourhero.ourweapon.dur += rep
    if ourhero.ourweapon.dur > ourhero.ourweapon.maxdur:
        ourhero.ourweapon.dur = ourhero.ourweapon.maxdur
    ourhero.activeitem = 0
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
    ourhero = newhero()

    # Make a basic weapon
    ourhero.ourweapon = ourhero.newweapon()

    # Make a basic armor
    ourhero.ourarmor = ourhero.newarmor()

    # Make a basic shield
    ourhero.ourshield = ourhero.newshield()

    # Make a potion
    ourhero.ouritem = ourhero.newitem()

    # apply our equipped items stats
    ourhero.applyequip()

    # make a basic enemy object
    ourenemy = getenemy()

    ourhero.name = input('Your name, ' + str(ourhero.ourclass) + '?\n')

    ourhero.heroperks()

    gameloop()
