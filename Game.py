import datetime
import os
import pickle
import random
import time
from sqlite3 import connect
import textwrap
import Enemy
import Hero
import dbsetup

suspensemode = 0
debugging = 0
autoattack = 0
armorbuff = .2


# TODO: Rewrite in full OOP, and separate / simplify get rid of spaghetti in Game.py

# One round of a battle
def battle():
    global ourhero
    global ourenemy
    ourhero.battlecount += 1
    printaversaries()
    marqueeprint('[BATTLE]')
    centerprint('[a]tk  [d]ef [r]un [i]tem')
    centerprint('Coinflip to [h]eal (100g)')
    centerprint('Action?')
    nextmove = input()

    # Used for auto attack
    if autoattack:
        nextmove = 'a'

    if ourhero.isalive():
        playerturn(nextmove)
    if ourenemy.isalive():
        enemyturn()
    if not ourhero.isalive():
        ourhero.isbattling = False
        marqueeprint('YOU DIED')
        centerprint('Cause of death:')
        centerprint('lvl ' + str(ourenemy.level) + ' ' + str(ourenemy.name))
        ourhero.printheroinfodetail()
        quit()
    if not ourenemy.isalive():
        ourhero.isbattling = False
        ourenemy.reset()
        hpback = int(ourhero.maxhp * .2)
        marqueeprint('[VICTORY]')
        centerprint('You gained ' + str(ourenemy.xp) + ' Exp')
        centerprint('You earned ' + str(ourenemy.gold) + ' Gold')
        # 20% chance to get some health back.
        if random.randrange(0, 6) == 0:
            centerprint('You found some food. You gained')
            centerprint(str(hpback) + ' HP back')
            ourhero.hp += hpback
            if ourhero.hp > ourhero.maxhp:
                ourhero.hp = ourhero.maxhp

        ourhero.xp += ourenemy.xp
        ourhero.gold += ourenemy.gold
        if ourhero.xp >= ourhero.nextlevel:
            ourhero.levelup()
    if not ourhero.isbattling:
        return


def playerturn(m):
    global ourhero
    global ourenemy
    marqueeprint('[HERO TURN]')
    ourhero.defn = ourhero.basedef + ourhero.ourarmor.basedefn + ourhero.ourshield.basedefn
    crit = 0
    critchance = random.randrange(0, 20)
    if critchance == 0:
        crit = ourhero.atk * .4
    effatk = int(ourhero.atk + crit - ourenemy.defn * armorbuff)
    if effatk < 0:
        effatk = 0
    if m == 'a' or m == '':
        if critchance == 0:
            centerprint('CRITICAL HIT!')
        ourenemy.hp = ourenemy.hp - effatk
        ourhero.ourweapon.dur -= int(effatk * .01)
        if ourenemy.hp < 0:
            ourenemy.hp = 0
            ourhero.isbattling = False
        centerprint(str(ourhero.name) + ' attacks ' + str(ourenemy.name))
        centerprint('for ' + str(effatk) + ' damage!')
    elif m == 'd':
        marqueeprint('[DEFENSE]')
        ourhero.defn += ourhero.defn * armorbuff
    elif m == 'r':
        marqueeprint('[RUN ATTEMPT]')
        rand = random.randrange(0, 4)
        if rand == 0:
            centerprint('you ran away')
            ourhero.isbattling = False
            return
        else:
            centerprint('you can\'t run!')
    elif m == 'i':
        item_management()
    elif m == 'h':
        marqueeprint('[HEAL]')
        centerprint('Death appears to flip a coin with you.')
        if ourhero.gold >= 100:
            ourhero.gold -= 100
            newrand = random.randrange(0, 1)
            if newrand == 0:
                ourhero.hp = ourhero.maxhp + ourhero.hpaug
                marqueeprint('[HEAL SUCCESS]')
                centerprint(str(ourhero.hp) + ' healed')
            else:
                marqueeprint('HEAL FAILED\nYou lost the roll!\n')
        else:
            marqueeprint('[HEAL FAILED]')
            centerprint('You don\'t have enough money!')
    marqueeprint('[END TURN]')
    wait = input()
    # accounts for health regen potion
    if ourhero.regentimer > 0:
        regen = int(ourhero.hp * .2)
        centerprint('You regen ' + str(regen) + 'HP')
        ourhero.hp += regen
        ourhero.regentimer -= 1
        if ourhero.hp > ourhero.maxhp:
            ourhero.hp = ourhero.maxhp

    # accounts for haste potion for 5 turn dodge increases
    ourhero.dodge = ourhero.basedodge
    if ourhero.hastetimer > 0:
        ourhero.dodge = ourhero.basedodge + 2
        centerprint('Your dodge chance is elevated')
        ourhero.hastetimer -= 1
    else:
        ourhero.dodge = ourhero.basedodge


def enemyturn():
    global ourhero
    global ourenemy
    overunder = random.randrange(0, 20)
    if ourenemy.isalive:
        marqueeprint('[ENEMY TURN]')
        if overunder == 0:
            ourenemy.atk += ourenemy.atk * .2
            centerprint(str(ourenemy.name) + ' got Angrier!')
        elif overunder == 1:
            ourenemy.atk -= ourenemy.atk * .2
            centerprint(str(ourenemy.name) + ' got Weaker!')
        elif overunder == 2:
            centerprint(str(ourenemy.name) + ' ran away!')
            ourenemy.hp = 0
            ourhero.isbattling = False
            return
        if overunder in range(3, ourhero.dodge):
            centerprint(str(ourenemy.name) + ' swings and misses!')
            marqueeprint('[END TURN]')
            wait = input()
            return
        if ourhero.isbattling:
            effatk = int(ourenemy.atk - (armorbuff * ourhero.defn))
            if effatk < 0:
                effatk = 0
            centerprint(str(ourenemy.name) + ' attacks ' + str(ourhero.name))
            centerprint(' for ' + str(effatk) + ' damage!')
            ourhero.ourarmor.dur -= int(effatk * .02)
            ourhero.ourshield.dur -= int(effatk * .02)
            ourhero.hp = ourhero.hp - effatk
            marqueeprint('[END TURN]')
            wait = input()


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
    centerprint('[CHOOSE CLASS]')
    centerprint('[w]arrior [m]age [h]unter')
    ourclass = input()
    if ourclass == 'w' or ourclass == '':
        ourclass = 'warrior'
    elif ourclass == 'm':
        ourclass = 'mage'
    elif ourclass == 'h':
        ourclass = 'hunter'
    else:
        centerprint('Please enter a valid selection')
    new_hero_data = rows[0]
    ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2],
                           new_hero_data[3], new_hero_data[4], new_hero_data[5])
    return ournewhero


def blacksmith():
    global ourhero
    centerprint('An old Blacksmith rests at your camp')
    centerprint('He shows his wares and services:')
    centerprint('[f]ix gear [b]uy gear')
    nextdecision = input()
    if nextdecision == 'f':
        # offer equipment repair for any of the 3 slots, for 1g/durability point
        centerprint('The Blacksmith can offer repair ')
        centerprint('services for 1g/repair point')
        centerprint('Here is your gear durability:')
        print('Slot|\tName\t\t|\tDur\t\t|\tBroken?')
        print(
            str(1) + '\t|' + str(ourhero.ourshield.name) + ' ' + str(ourhero.ourshield.type) + '\t\t' + str(
                ourhero.ourshield.dur) + '/' + str(
                ourhero.ourshield.maxdur) + '\t' + str(ourhero.ourshield.isbroken()))
        print(
            str(2) + '\t|' + str(ourhero.ourweapon.name) + ' ' + str(ourhero.ourweapon.type) + '\t\t' + str(
                ourhero.ourweapon.dur) + '/' + str(
                ourhero.ourweapon.maxdur) + '\t' + str(ourhero.ourweapon.isbroken()))
        print(str(3) + '\t|' + str(ourhero.ourarmor.name) + ' ' + str(ourhero.ourarmor.type) + '\t\t' + str(
            ourhero.ourarmor.dur) + '/' + str(
            ourhero.ourarmor.maxdur) + '\t' + str(ourhero.ourarmor.isbroken()))
        decision = input('What do you want to repair? [a] for all')
        if decision == '1' or decision == 'a':
            repaircost = ourhero.ourshield.maxdur - ourhero.ourshield.dur
            centerprint('Repair Your shield?')
            centerprint('Cost: ' + str(repaircost) + ' gold')
            centerprint('[y]es [n]o')
            decision2 = input()
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourshield.dur = ourhero.ourshield.maxdur
                centerprint('Repair Success.')
        if decision == '2' or decision == 'a':
            repaircost = ourhero.ourweapon.maxdur - ourhero.ourweapon.dur
            centerprint('Repair Your weapon?')
            centerprint('Cost: ' + str(repaircost) + ' gold')
            centerprint('[y]es [n]o')
            decision2 = input()
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourweapon.dur = ourhero.ourweapon.maxdur
                centerprint('Repair Success.')
        if decision == '3' or decision == 'a':
            repaircost = ourhero.ourarmor.maxdur - ourhero.ourarmor.dur
            centerprint('Repair Your armor?)')
            centerprint('Cost: ' + str(repaircost) + ' gold')
            centerprint('[y]es [n]o')
            decision2 = input()
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourarmor.dur = ourhero.ourarmor.maxdur
                centerprint('Repair Success')
    if nextdecision == 'b':
        weaponforsale = ourhero.newweapon()
        armorforsale = ourhero.newarmor()
        shieldforsale = ourhero.newshield()

        marqueeprint('[YOUR GEAR]')
        leftprint(str(1) + ' \tName: ' + str(ourhero.ourweapon.name)+ ' ' + str(ourhero.ourweapon.type) + '\tAttack: ' + str(ourhero.ourweapon.atk) + '\tCost: ' + str(ourhero.ourweapon.level * 61))
        leftprint(str(2) + ' \tName: ' + str(ourhero.ourarmor.name) + ' ' + str(ourhero.ourarmor.type)+ '\tDefense: ' + str(ourhero.ourarmor.name) + '\tCost: ' + str(ourhero.ourarmor.level* 57))
        leftprint(str(3) + ' \tName: ' + str(ourhero.ourshield.name)+ ' ' + str(ourhero.ourshield.type) + '\tDefense: ' + str(ourhero.ourshield.name) + '\tCost: ' + str(ourhero.ourshield.level* 53))

        wepcost = weaponforsale.level * 38
        armcost = armorforsale.level * 29
        shcost = shieldforsale.level * 43


        marqueeprint('[GEAR FOR SALE]')
        leftprint(str(1) + ' \tName: ' + str(weaponforsale.name) + ' ' + str(weaponforsale.type) + '\tAttack: ' + str(weaponforsale.atk) + '\tCost: ' + str(wepcost))
        leftprint(str(2) + ' \tName: ' + str(shieldforsale.name) + ' ' + str(shieldforsale.type) + '\tDefense: ' + str(shieldforsale.name) + '\tCost: ' + str(shcost))
        leftprint(str(3) + ' \tName: ' + str(armorforsale.name) + ' ' + str(armorforsale.type) + '\tDefense: ' + str(armorforsale.name) + '\tCost: ' + str(armcost))
        centerprint('Please enter decision')
        itemindex = input()
        if itemindex not in ['1', '2', '3']:
            centerprint('Please enter a valid choice')
            return
        if itemindex == '1':
            ourhero.ourweapon = weaponforsale
            if ourhero.gold <wepcost:
                centerprint('You don\'t have enough money!')
            ourhero.gold -= wepcost
            centerprint('You equip your new gear: ' + str(weaponforsale.name) + ' ' + str(weaponforsale.type))
        if itemindex == '2':
            ourhero.ourshield = shieldforsale
            if ourhero.gold <wepcost:
                centerprint('You don\'t have enough money!')
            ourhero.gold -= armcost
            centerprint('You equip your new gear: ' + str(shieldforsale.name) + ' ' + str(shieldforsale.type))
        if itemindex == '3':
            ourhero.ourarmor = armorforsale
            if ourhero.gold <shcost:
                centerprint('You don\'t have enough money!')
            ourhero.gold -= shcost
            centerprint('You equip your new gear: ' + str(armorforsale.name) + ' ' + str(armorforsale.type))
        return
        # offer random choice of weapon, armor, or shield at 1.5x value price


# show one item, one
def store():
    global ourweapon
    global ourarmor
    global ourshield
    global ouritem


def camp():
    global ourhero
    marqueeprint('[CAMP]')
    centerprint('[a]dventure [r]est [i]tem [e]quip [h]ero')
    centerprint('[p]eddler [b]lacksmith [l]oad [s]ave [q]uit')
    m = input()
    if m == 'r':
        marqueeprint('[RESTING]')
        ourhero.hp = (ourhero.maxhp + ourhero.hpaug)
        centerprint('Hero HP: ' + str(ourhero.hp))
        return
    elif m == 'i':
        marqueeprint('[ITEMS]')
        item_management()
        return
    elif m == 'e':
        marqueeprint('[GEAR]')
        gear_management()
    elif m == 'h':
        marqueeprint('[HERO DETAIL]')
        ourhero.printheroinfodetail()
        ourhero.ourweapon.printweaponinfo()
        ourhero.ourshield.printshieldinfo()
        ourhero.ourarmor.printarmorinfo()
    elif m == 'a':
        marqueeprint('[ADVENTURE]')
        adventure()
    elif m == 'l':
        marqueeprint('[LOADGAME]')
        loadgame()
    elif m == 's':
        marqueeprint('[SAVEGAME]')
        savegame()
    elif m == 'b':
        marqueeprint('[BLACKSMITH]')
        blacksmith()
    elif m == 'p':
        marqueeprint('[PEDDLER\'S WARES]')
        centerprint('An old Peddler rests at your camp.\nHe shows his wares:')
        nextdecision = input()
        if nextdecision == 'b':
            # offer random choice of weapon, armor, or shield at 1.5x value price
            pass
    elif m == 'q':
        marqueeprint('[QUIT]')
        decision = input('Are you sure?')
        if decision == 'y':
            quit()
    else:
        centerprint('You walk back to camp')


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


def item_management():
    global ourhero
    marqueeprint('[CHOOSE ITEM]')
    for i, item in enumerate(ourhero.items):
        print(str(i) + ' \tName: ' + str(item.name) + '\tEffect: ' + str(item.effect))
    centerprint('Please enter decision')
    itemindex = input()
    if itemindex not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                         '17', '18', '19', '20']:
        centerprint('Please enter a valid choice')
        return
    ourhero.ouritem = ourhero.items[int(itemindex)]
    ourhero.activeitem = ourhero.ouritem
    del (ourhero.items[int(itemindex)])
    centerprint('Using ' + str(ourhero.ouritem.name))
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


# TODO: DOESN'T WORK
def gear_management():
    global ourshield
    global ourweapon
    global ourarmor
    print(str(1) + ourshield.name + '\n' + str(2) + ourweapon.name + '\n' + str(3) + ourarmor.name + '\n')


def gameloop():
    while True:
        adventure()


def adventure():
    global ourenemy
    global ourhero
    marqueeprint('[ADVENTURE]')
    centerprint('[a]dventure or [c]amp')
    m = input()
    ourrand = random.randint(0, 100)

    if m == 'a' or m == '':
        if ourrand <= 75 and False:
            ourhero.isbattling = True
            # Make new enemy
            ourenemy = getenemy()
            marqueeprint('[BATTLE]')
            # battle until one is dead
            turnnum = 1
            while ourhero.isalive() and ourenemy.isalive() and ourhero.isbattling:
                marqueeprint('[TURN ' + str(turnnum) + ']')
                battle()
                turnnum += 1
        elif 75 < ourrand <= 95 and False:
            marqueeprint('[FOUND ITEM!]')
            itemrand = random.randrange(0, 6)
            if itemrand == 0:
                ourhero.ourarmor = ourhero.newarmor()
                ourhero.ourarmor.printarmorinfo()
            elif itemrand == 1:
                ourhero.ourweapon = ourhero.newweapon()
                ourhero.ourweapon.printweaponinfo()
            elif itemrand == 2:
                ourhero.ourshield = ourhero.newshield()
                ourhero.ourshield.printshieldinfo()
            elif 3 <= itemrand <= 6:
                ourhero.ouritem = ourhero.newitem()
                ourhero.ouritem.printiteminfo()
                ourhero.items.append(ourhero.ouritem)
            ourhero.applyequip()
        elif 95 < ourrand <= 100:
            centerprint('You find a traveler,')
            centerprint('He says:')
            print('\n')
            with open('./quoteslist.txt', 'rb') as f:
                quotelist = f.read().splitlines()
                quote = random.choice(quotelist)
                quote = quote.decode('utf-8')
                wrapstring = textwrap.wrap(quote, width=48)
                for line in wrapstring:
                    centerprint(line)
                print('\n')
            centerprint('...you venture back to camp')
    elif m == 'c':
        camp()


def healingpotion():
    marqueeprint('[HEALING POTION]')
    global ourhero
    healed = ourhero.activeitem.effect
    ourhero.hp += healed
    centerprint('You heal for ' + str(healed) + ' HP')
    if ourhero.hp > ourhero.maxhp:
        ourhero.hp = ourhero.maxhp
        ourhero.activeitem = 0
    return


def explosivemanavial():
    marqueeprint('[EXPLOSIVE MANA BOMB]')
    global ourhero
    global ourenemy
    dmg = ourhero.activeitem.effect
    ourenemy.hp -= ourhero.activeitem.effect
    centerprint('The Mana Vial EXPLODES!')
    centerprint('Dealing ' + str(dmg) + ' damage to ' + str(ourenemy.name))
    ourhero.activeitem = 0
    return


# adds health per turn
def healthregenpotion():
    marqueeprint('[REGEN POTION]')
    global ourhero
    centerprint('5 turns health regen')
    ourhero.regentimer = 5
    ourhero.activeitem = 0


# dodge buff
def hastepotion():
    marqueeprint('[HASTE POTION]')
    global ourhero
    centerprint('5 turns dodge buff')
    ourhero.hastetimer = 5
    ourhero.activeitem = 0


# heals 60% of dur points to weapon
def weaponrepairtincture():
    marqueeprint('[WEAPON REPAIR]')
    global ourhero
    rep = ourhero.ourweapon.maxdur * .6
    centerprint('You repaired your weapon for\n' + str(rep) + ' durability points')
    ourhero.ourweapon.dur += rep
    if ourhero.ourweapon.dur > ourhero.ourweapon.maxdur:
        ourhero.ourweapon.dur = ourhero.ourweapon.maxdur
    ourhero.activeitem = 0


# adds a little suspense to offset the monotony of text input
def suspense():
    s = '.'
    if suspensemode:
        time.sleep(.1)


def marqueeprint(text):
    print('{:=^50}'.format(text))


def leftprint(text):
    print('{:<50}'.format(text))


def rightprint(text):
    print('{:>50}'.format(text))


def centerprint(text):
    print('{:^50}'.format(text))


def printtest():
    marqueeprint("[[PRINT TEST]]")
    leftprint('Justified Left')
    rightprint('Justified Right')
    centerprint('Center Print')


def printaversaries():
    global ourhero
    global ourenemy
    print(lr_justify('[HERO]', '[ENEMY]', 50))
    print(lr_justify(ourhero.name, ourenemy.name, 50))
    print(lr_justify(str('lvl: ' + str(ourhero.level)), str('lvl: ' + str(ourenemy.level)), 50))
    print(lr_justify(str('HP: ' + str(ourhero.hp)), str('HP: ' + str(ourenemy.hp)), 50))
    print(lr_justify(str('XP: ' + str(ourhero.xp) + '/' + str(ourhero.nextlevel)), str('XP drop: ' + str(ourenemy.xp)), 50))


def lr_justify(left, right, width):
    return '{}{}{}'.format(left, ' ' * (width - len(left + right)), right)


if __name__ == '__main__':
    # this is for repopulating the database with modified CSV files
    # TODO: Make so database will not append if run more than once
    # Create all game databases (only needs to run once to make databases)

    debugging = input('Enter Debugging Mode?\n[1] for yes\nENTER for no\n')
    # re-creates the database, in case you change values1
    if debugging:
        printtest()
        print('Reload database?')
        dbreload = input('[y]es [n]o\n')
        if dbreload == 'y':
            oursetup = dbsetup.dbsetup()
            oursetup.setupdb()
    marqueeprint('')
    centerprint('MiniRPG')
    centerprint('Colin Burke 2017')
    marqueeprint('')

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

    centerprint('Your name, ' + str(ourhero.ourclass) + '?\n')
    ourhero.name = input()

    ourhero.heroperks()

    gameloop()
