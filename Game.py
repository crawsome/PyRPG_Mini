import datetime
import os
import pickle
import random
import textwrap
import time
from difflib import SequenceMatcher
from sqlite3 import connect

import Enemy
import Hero
import dbsetup

# adds a little suspense
suspensemode = 0

# provides inner workings of game, some live-comments
debugging = 0

# provides a way to speed through battle (risky!)
autoattack = 0


# TODO: make ourhero.levelup and newhero the same function

# makes a new hero object for when starting new game.
def newhero():
    conn.execute('SELECT * FROM levelnotes WHERE level = 1;')
    rows = conn.fetchall()
    marqueeprint('[CHOOSE CLASS]')
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
    marqueeprint('[CHOOSE DIFFICULTY]')
    centerprint('[1]easy [2]med [3]hard')
    diff = input()
    if diff == '1' or diff == '':
        diffcurve = .4
        handicap = .05
    elif diff == '2':
        diffcurve = .2
        handicap = .2
    elif diff == '3':
        diffcurve = .05
        handicap = .4
    else:
        centerprint('Please enter a valid selection')
        diff = 1
        diffcurve = .4
        centerprint('Setting Difficulty to ' + str(diff))

    new_hero_data = rows[0]
    ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2],
                           new_hero_data[3], new_hero_data[4], new_hero_data[5])
    ournewhero.diffcurve = diffcurve
    marqueeprint('ENTER NAME')
    centerprint('Your name, ' + str(ournewhero.ourclass) + '?\n')
    ournewhero.name = input()
    if ournewhero.name == '':
        ournewhero.name = 'Sir Lazy of Flabgard'

    return ournewhero


# brings game back after death.
def gameloop():
    while True:
        marqueeprint('')
        centerprint('MiniRPG')
        centerprint('Colin Burke 2017')
        marqueeprint('')
        centerprint('[n]ew game [l]oad')
        decision = input()

        if decision == 'n' or decision == '':
            # Make new global hero and enemy which will change over time
            ourhero = newhero()
            ourenemy = getenemy(ourhero)

            ourhero.heroperks()
            ourhero.printheroinfodetail()
        if decision == 'l':
            print('lOADING GAME')
            ourhero = loadgame()
            ourenemy = getenemy(ourhero)
        while ourhero.isalive():
            adventure(ourhero, ourenemy)


# where the meat of things happen, this decides what happens when you enter [a]dventure
def adventure(ourhero, ourenemy):
    centerprint('[a]dventure or [c]amp')
    m = input()
    ourrand = random.randint(0, 100)
    if m == 'a' or m == '':
        if ourrand <= 70:
            ourhero.isbattling = True
            # Make new enemy
            ourenemy = getenemy(ourhero)
            marqueeprint('[BATTLE]')
            print('')
            # battle until one is dead
            turnnum = 1
            while ourhero.isalive() and ourenemy.isalive() and ourhero.isbattling:
                marqueeprint('[TURN ' + str(turnnum) + ']')
                battle(ourhero, ourenemy)
                turnnum += 1
        elif 70 < ourrand <= 90:
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
        elif 90 < ourrand <= 95:
            marqueeprint('A LONE TRAVELER')
            centerprint('You find a lone traveler,')
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
            threechoicerandom = random.randrange(0, 2)
            if threechoicerandom == 0:
                xpgain = int(ourhero.xp * .10)
                ourhero.addxp(int(round(xpgain, 1)))
            if threechoicerandom == 1:
                goldgain = int(ourhero.gold * .10)
                ourhero.addgold(goldgain)
            if threechoicerandom == 2:
                pass
            centerprint('...you venture back to camp')
        elif 90 < ourrand <= 95:
            # a story event?
            pass
        elif 95 < ourrand <= 100:
            marqueeprint('[RIDDLE]')
            centerprint('The area gets quiet. The wind blows.')
            centerprint('A torn page lands in your grasp. It reads:')
            print('')
            ourriddle = getriddle()
            wrapstring = textwrap.wrap(ourriddle[0], width=48)
            answer = str(ourriddle[1]).lower()
            for line in wrapstring:
                centerprint(line)
            print('')
            centerprint('Speak the answer to the wind...')
            useranswer = input()
            if useranswer == '':
                while (useranswer == ''):
                    centerprint('Please answer the riddle.')
                    useranswer = input()
                    if debugging:
                        print(answer + ', you cheater!')
            if similarstring(useranswer, answer) and useranswer != '':
                centerprint('You have successfully answered the riddle')
                centerprint('The answer was \"' + answer + '\"')
                centerprint('I present you with this:')
                ourhero.addgold(ourhero.level * 40)
                ourhero.addxp(ourhero.nextlevel * .4)
            else:
                centerprint('You Fail! Leave this place!')

    elif m == 'c':
        print('')
        camp(ourhero, ourenemy)
    if not ourhero.isalive():
        return


# One round of a battle
def battle(ourhero, ourenemy):
    ourhero.battlecount += 1
    printadversaries(ourhero, ourenemy)
    print('')
    marqueeprint('[CHOOSE ACTION]')
    centerprint('[a]tk  [d]ef [r]un [i]tem')
    centerprint('Coinflip to [h]eal (100g)')
    centerprint('Action?')
    nextmove = input()
    # conditions to end battle
    if ourhero.isalive():
        playerturn(ourhero, ourenemy, nextmove)
    if ourenemy.isalive():
        enemyturn(ourhero, ourenemy)
    if not ourhero.isalive():
        ourhero.death()
        return
    if not ourenemy.isalive():
        ourhero.isbattling = False
        ourenemy.reset()
        marqueeprint('[VICTORY]')
        ourhero.addgold(ourenemy.gold + (ourenemy.gold * ourhero.diffcurve))
        ourhero.addxp(ourenemy.xp + (ourenemy.xp * ourhero.diffcurve))
        # 15% chance to get some health back.
        print('')
        if random.randrange(0, 100) in range(0, 15):
            ourhero.food()
    if not ourhero.isbattling:
        return
        wait = input()


# One round of a player's turn
def playerturn(ourhero, ourenemy, m):
    marqueeprint('[HERO TURN]')
    crit = 0
    critrand = random.randrange(0, 100)
    if critrand in range(ourhero.crit, critrand):
        crit = ourhero.atk * .4
    effatk = int(ourhero.atk + crit - (ourenemy.defn * ourhero.diffcurve))
    if debugging:
        centerprint('playerattack(' + str(ourhero.atk) + ') + crit(' + str(crit) + ') -')
        centerprint('(ourhero.diffcurve(' + str(ourhero.diffcurve) + ') * Enemy def(' + str(ourenemy.defn) + '))')
    if effatk < 0:
        effatk = 0
    if m == 'a' or m == '':
        if critrand == 0:
            centerprint('CRITICAL HIT!')
        ourenemy.damage(effatk)
        ourhero.ourweapon.damagedur(effatk, .01)
        if ourenemy.hp < 0:
            ourenemy.hp = 0
            ourhero.isbattling = False
        centerprint(str(ourhero.name) + ' attacks ' + str(ourenemy.name))
        centerprint('for ' + str(effatk) + ' damage!')
    elif m == 'd':
        marqueeprint('[DEFENSE]')
        ourhero.defn += ourhero.defn * ourhero.diffcurve
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
        item_management(ourhero, ourenemy)
    elif m == 'h':
        ourhero.healflip()
    wait = input()

    # for health regen potion
    if ourhero.regentimer > 0:
        regen = int(ourhero.hp * .2)
        centerprint('You regen ' + str(regen) + 'HP')
        ourhero.heal(regen)
        ourhero.regentimer -= 1

    # for haste potion for 5 turn dodge increases
    ourhero.dodge = ourhero.basedodge
    if ourhero.hastetimer > 0:
        ourhero.dodge = ourhero.basedodge + 5
        centerprint('Your dodge chance is elevated')
        ourhero.hastetimer -= 1
    else:
        ourhero.dodge = ourhero.basedodge


# One round of an enemy turn
def enemyturn(ourhero, ourenemy):
    overunder = random.randrange(0, 20)
    if ourenemy.isalive:
        marqueeprint('[ENEMY TURN]')
        if overunder == 0:
            ourenemy.anger()
            wait = input()
        elif overunder == 1:
            ourenemy.weaker()
            wait = input()
        elif overunder == 2:
            centerprint(str(ourenemy.name) + ' ran away!')
            ourenemy.hp = 0
            ourhero.isbattling = False
            wait = input()
            return
        if overunder in range(3, ourhero.dodge):
            centerprint(str(ourenemy.name) + ' swings and misses!')
            wait = input()
            return
        if ourhero.isbattling:
            effatk = int(ourenemy.atk - (ourhero.diffcurve * ourhero.defn))
            if effatk < 0:
                effatk = 0
            if debugging:
                centerprint('Enemy attack(' + str(ourenemy.atk) + ') -')
                centerprint(
                    'ourhero.diffcurve(' + (str(ourhero.diffcurve) + ') * (hero def(' + str(ourhero.defn) + ')'))
            centerprint(str(ourenemy.name) + ' attacks ' + str(ourhero.name))
            centerprint(' for ' + str(effatk) + ' damage!')
            ourhero.ourarmor.dur -= int(effatk * ourhero.diffcurve)
            ourhero.ourshield.dur -= int(effatk * ourhero.diffcurve)
            ourhero.hp = ourhero.hp - effatk
            wait = input()


# fetch a random riddle from db
def getriddle():
    conn.execute('SELECT * FROM riddles ORDER BY RANDOM() LIMIT 1' + ';')
    row = conn.fetchall()[0]
    riddle = [row[0], row[1]]
    return riddle
    pass


# fetch a new enemy that is at hero's level (for now...)
def getenemy(ourhero):
    conn.execute('SELECT * FROM enemies WHERE level = ' + str(ourhero.level) + ';')
    rows = conn.fetchall()
    new_enemy = random.choice(rows)
    # create random enemy name
    levelname = random.choice((rows[0][1], rows[1][1], rows[2][1], rows[3][1], rows[4][1]))
    adjective = random.choice((rows[0][2], rows[1][2], rows[2][2], rows[3][2], rows[4][2]))
    enemyname = random.choice((rows[0][3], rows[1][3], rows[2][3], rows[3][3], rows[4][3]))
    ournewenemy = Enemy.Enemy(new_enemy[0], levelname, adjective, enemyname, new_enemy[4], new_enemy[5],
                              (new_enemy[6] + (new_enemy[6] * ourhero.diffcurve)), new_enemy[7], new_enemy[8],
                              new_enemy[9])
    return ournewenemy


# a blacksmith who can repair or sell gear
def blacksmith(ourhero):
    centerprint('An old Blacksmith rests at your camp')
    centerprint('He shows his wares and services:')
    centerprint('[f]ix gear [b]uy gear')
    nextdecision = input()
    centerprint('Gold: ' + str(ourhero.gold))
    if nextdecision == 'f':
        # offer equipment repair for any of the 3 slots, for 1g/durability point
        centerprint('The Blacksmith can offer repair ')
        centerprint('services for 1g/repair point')
        centerprint('Here is your gear durability:')
        data1 = ['Slot', 'Name', 'Dur', 'Broken?']
        data2 = [str(1), str(ourhero.ourweapon.name) + str(ourhero.ourweapon.type),
                 str(ourhero.ourweapon.dur) + '/' + str(ourhero.ourweapon.maxdur), str(ourhero.ourweapon.isbroken())]
        data3 = [str(2), str(ourhero.ourshield.name) + ' ' + str(ourhero.ourshield.type),
                 str(ourhero.ourshield.dur) + '/' + str(ourhero.ourshield.maxdur), str(ourhero.ourshield.isbroken())]
        data4 = [str(3), str(ourhero.ourarmor.name) + ' ' + str(ourhero.ourarmor.type),
                 str(ourhero.ourarmor.dur) + '/' + str(ourhero.ourarmor.maxdur), str(ourhero.ourarmor.isbroken())]

        decision = input('What do you want to repair? [a] for all')
        if decision == '1' or decision == 'a':
            repaircost = ourhero.ourweapon.maxdur - ourhero.ourweapon.dur
            centerprint('Repair Your weapon?')
            centerprint('Cost: ' + str(repaircost) + ' gold')
            centerprint('[y]es [n]o')
            decision2 = input()
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourweapon.dur = ourhero.ourweapon.maxdur
                centerprint('Repair Success.')
        if decision == '2' or decision == 'a':
            repaircost = ourhero.ourshield.maxdur - ourhero.ourshield.dur
            centerprint('Repair Your shield?')
            centerprint('Cost: ' + str(repaircost) + ' gold')
            centerprint('[y]es [n]o')
            decision2 = input()
            if decision2 == 'y' and ourhero.gold >= repaircost:
                ourhero.gold -= repaircost
                ourhero.ourshield.dur = ourhero.ourshield.maxdur
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
    # offer random choice of weapon, armor, or shield at 1.5x value price
    elif nextdecision == 'b':
        weaponforsale = ourhero.newweapon()
        armorforsale = ourhero.newarmor()
        shieldforsale = ourhero.newshield()
        marqueeprint('[YOUR GEAR]')
        leftprint(
            str(1) + ' \tName: ' + str(ourhero.ourweapon.name) + ' ' + str(ourhero.ourweapon.type) + '\tAttack: ' + str(
                ourhero.ourweapon.atk) + '\tCost: ' + str(ourhero.ourweapon.level * 50 * ourhero.diffcurve))
        leftprint(str(2) + ' \tName: ' + str(ourhero.ourshield.name) + ' ' + str(
            ourhero.ourshield.type) + '\tDefense: ' + str(ourhero.ourshield.defn) + '\tCost: ' + str(
            ourhero.ourshield.level * 50 * ourhero.diffcurve))
        leftprint(
            str(3) + ' \tName: ' + str(ourhero.ourarmor.name) + ' ' + str(ourhero.ourarmor.type) + '\tDefense: ' + str(
                ourhero.ourarmor.defn) + '\tCost: ' + str(ourhero.ourarmor.level * 50 * ourhero.diffcurve))
        print('\n')
        # determine weapon coses
        wepcost = weaponforsale.level * 50 * ourhero.diffcurve
        armcost = armorforsale.level * 50 * ourhero.diffcurve
        shcost = shieldforsale.level * 50 * ourhero.diffcurve
        marqueeprint('[GEAR FOR SALE]')
        leftprint(str(1) + ' \tName: ' + str(weaponforsale.name) + ' ' + str(weaponforsale.type) + '\tAttack: ' + str(
            weaponforsale.atk) + '\tCost: ' + str(wepcost))
        leftprint(str(2) + ' \tName: ' + str(shieldforsale.name) + ' ' + str(shieldforsale.type) + '\tDefense: ' + str(
            shieldforsale.defn) + '\tCost: ' + str(shcost))
        leftprint(str(3) + ' \tName: ' + str(armorforsale.name) + ' ' + str(armorforsale.type) + '\tDefense: ' + str(
            armorforsale.defn) + '\tCost: ' + str(armcost))
        centerprint('Please enter decision')
        itemindex = input()
        if itemindex not in ['1', '2', '3']:
            centerprint('Please enter a valid choice')
        elif itemindex == '1':
            ourhero.ourweapon = weaponforsale
            if ourhero.gold < wepcost:
                centerprint('You don\'t have enough money!')
            ourhero.gold -= wepcost
            centerprint('You equip your new gear: ' + str(weaponforsale.name) + ' ' + str(weaponforsale.type))
        elif itemindex == '2':
            ourhero.ourshield = shieldforsale
            if ourhero.gold < wepcost:
                centerprint('You don\'t have enough money!')
                return
            ourhero.gold -= armcost
            centerprint('You equip your new gear: ' + str(shieldforsale.name) + ' ' + str(shieldforsale.type))
        elif itemindex == '3':
            ourhero.ourarmor = armorforsale
            if ourhero.gold < shcost:
                centerprint('You don\'t have enough money!')
                return
            ourhero.gold -= shcost
            centerprint('You equip your new gear: ' + str(armorforsale.name) + ' ' + str(armorforsale.type))
        ourhero.applyequip()
        return


# a camp where you regain hp after so many fights.
def camp(ourhero, ourenemy):
    ourhero.hp = ourhero.maxhp
    marqueeprint('[CAMP]')
    centerprint('You rest at camp. Hero HP: ' + str(ourhero.hp))
    centerprint('[a]dventure [i]tem [h]ero')
    centerprint('[p]eddler [b]lacksmith')
    centerprint('[l]oad [s]ave [q]uit')
    m = input()
    if m == 'i':
        marqueeprint('[ITEMS]')
        item_management(ourhero, ourenemy)
        return
    elif m == 'h':
        marqueeprint('[HERO DETAIL]')
        ourhero.printheroinfodetail()
        wait = input()
        ourhero.ourweapon.printweaponinfo()
        wait = input()
        ourhero.ourshield.printshieldinfo()
        wait = input()
        ourhero.ourarmor.printarmorinfo()
        wait = input()
    elif m == 'a':
        return
        # adventure(ourhero, ourenemy)
    elif m == 'l':
        marqueeprint('[LOADGAME]')
        ourhero = loadgame()
    elif m == 's':
        marqueeprint('[SAVEGAME]')
        savegame(ourhero)
    elif m == 'b':
        marqueeprint('[BLACKSMITH]')
        blacksmith(ourhero)
    elif m == 'p':
        marqueeprint('[PEDDLER\'S WARES]')
        peddler(ourhero)
    elif m == 'q':
        marqueeprint('[QUIT]')
        decision = input('Are you sure?')
        if decision == 'y':
            quit()
    else:
        centerprint('You walk back to camp')


# sell the hero items (will be able to buy soon)
def peddler(ourhero):
    centerprint('An old Peddler rests at your camp.')
    centerprint('He shows his wares:')
    centerprint('[b]uy, [s]ell, [f]ortune-telling')
    nextdecision = input()
    if nextdecision == 'b':
        pass
        item1 = ourhero.newitem()
        item2 = ourhero.newitem()
        item3 = ourhero.newitem()
        item4 = ourhero.newitem()
        item5 = ourhero.newitem()
        itemarray = [item1, item2, item3, item4, item5]
        for i, item in enumerate(itemarray):
            print(str(i + 1) + '\t' + item.name + '\t' + str(item.val * 1.5))
        print('Your selection? (ENTER to go back)')
        selection = input()
        if selection == '1':
            ourhero.buy(item1)
        elif selection == '2':
            ourhero.buy(item2)
        elif selection == '3':
            ourhero.buy(item3)
        elif selection == '4':
            ourhero.buy(item4)
        elif selection == '5':
            ourhero.buy(item5)
        elif selection == '':
            centerprint('\"WHYD YOU COME HERE AND NOT BUY ANYTHING?\"')
            return
        else:
            print('Get out of here you bum!')
            # offer random choice of items at 1.5x value price
    if nextdecision == 's':
        pass
        # let hero sell anything for .6 their value in gold.
    if nextdecision == 'f':
        pass
        # Tell hero a fortune, -/+ stats and -/+ luck possibility


# pickle in to hero obj and start gameloop
def loadgame():
    # load hero object from pickle file
    dirlist = os.listdir('./saves/')
    for i, item in enumerate(dirlist):
        print(str(i) + ' - ' + str(item))
        print(str(datetime.datetime.fromtimestamp(os.path.getmtime('./saves/' + item))))
        print('\n')
    index = input("Which Character?\nOr [c]ancel")
    if index == '':
        index = 0
    if index == 'c':
        return
    index = int(index)
    ourpickle = open(('./saves/' + str(dirlist[index])), "rb")
    ourdata = pickle.load(ourpickle)
    return ourdata


# pickle our hero to file
def savegame(ourhero):
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


# TODO: Go back from item menu without enemy turn happening
# TODO: Make this into an item selection method, with an argument if [s]elling, [u]sing, or [d]iscarding
# lets hero use items
def item_management(ourhero, ourenemy):
    invlimit = 20
    marqueeprint('[CHOOSE ITEM]')
    for i, item in enumerate(ourhero.items):
        print(str(i) + ' \tName: ' + str(item.name) + '\tEffect: ' + str(item.effect))
        if i > invlimit:
            break
    centerprint('Please enter decision')
    itemindex = int(input())
    if itemindex not in range(0, invlimit):
        centerprint('Please enter a valid choice')
        return
    ourhero.ouritem = ourhero.items[int(itemindex)]
    ourhero.activeitem = ourhero.ouritem
    del (ourhero.items[int(itemindex)])
    centerprint('Using ' + str(ourhero.ouritem.name))
    if ourhero.ouritem.name == 'Healing Potion':
        healingpotion(ourhero)
    if ourhero.ouritem.name == 'Explosive Mana Vial':
        explosivemanavial(ourhero, ourenemy)
    if ourhero.ouritem.name == 'Health Regen Potion':
        healthregenpotion(ourhero)
    if ourhero.ouritem.name == 'Haste Potion':
        hastepotion(ourhero)
    if ourhero.ouritem.name == 'Weapon Repair Tincture':
        weaponrepairtincture(ourhero)


# hero uses a healing potion
def healingpotion(ourhero):
    marqueeprint('[HEALING POTION]')
    healed = ourhero.activeitem.effect
    ourhero.heal(healed)
    ourhero.activeitem = 0
    return


# hero uses an item that damages enemy
def explosivemanavial(ourhero, ourenemy):
    marqueeprint('[EXPLOSIVE MANA BOMB]')
    centerprint('The Mana Vial EXPLODES!')
    dmg = ourhero.activeitem.effect
    centerprint('Dealing ' + str(dmg) + ' damage to ' + str(ourenemy.name))
    ourenemy.damage(ourhero.activeitem.effect)
    ourhero.activeitem = 0
    return


# adds health per turn
def healthregenpotion(ourhero):
    marqueeprint('[REGEN POTION]')
    ourhero.regentimer += 5
    centerprint(str(ourhero.regentimer) + ' turns health regen')
    ourhero.activeitem = 0


# dodge buff
def hastepotion(ourhero):
    marqueeprint('[HASTE POTION]')
    centerprint(str(ourhero.hastetimer) + ' turns dodge buff')
    ourhero.hastetimer += 5
    ourhero.activeitem = 0


# heals 60% of dur points to weapon
def weaponrepairtincture(ourhero):
    marqueeprint('[WEAPON REPAIR]')
    rep = ourhero.ourweapon.maxdur * .6
    centerprint('You repaired your weapon for ' + str(rep) + ' durability points')
    ourhero.ourweapon.dur += rep
    if ourhero.ourweapon.dur > ourhero.ourweapon.maxdur:
        ourhero.ourweapon.dur = ourhero.ourweapon.maxdur
    ourhero.activeitem = 0


# adds a little suspense to offset the monotony of text input
def suspense():
    s = ' '
    if suspensemode:
        time.sleep(.5)
        print(s)


# will print something with ==text==, centered
def marqueeprint(text):
    print('{:=^50}'.format(text))


# Left-justify print
def leftprint(text):
    print('{:<50}'.format(text))


# right-justify print
def rightprint(text):
    print('{:>50}'.format(text))


# centered print
def centerprint(text):
    wrapstring = textwrap.wrap(text, width=50)
    for line in wrapstring:
        #print(line)
        print('{:^50}'.format(line))


# From https://stackoverflow.com/questions/9640109/allign-left-and-right-in-python
def lr_justify(left, right, width):
    return '{}{}{}'.format(left, ' ' * (width - len(left + right)), right)


# Prints 4 rows of something
def fourrowprint(table_data, title):
    marqueeprint(title)
    for row in table_data:
        print("{: >12} {: >12} {: >12} {: >12}".format(*row))


# for debugging and margin adjustments for user to zoom in
def printtest():
    marqueeprint("[[PRINT TEST]]")
    leftprint('Justified Left')
    rightprint('Justified Right')
    centerprint('Center Print')


# Print hero and enemy justified on left and right
def printadversaries(ourhero, ourenemy):
    print(lr_justify('[HERO]', '[ENEMY]', 50))
    print(lr_justify(ourhero.name, ourenemy.name, 50))
    print(lr_justify(str('lvl: ' + str(ourhero.level)), str('lvl: ' + str(ourenemy.level)), 50))
    print(lr_justify(str('HP: ' + str(ourhero.hp) + '/' + str(ourhero.maxhp)),
                     str('HP: ' + str(ourenemy.hp) + '/' + str(ourenemy.maxhp)), 50))
    print(lr_justify(str('XP: ' + str(ourhero.xp) + '/' + str(ourhero.nextlevel)), str('XP drop: ' + str(ourenemy.xp)),
                     50))


# To be used on status screens
def printmarqueehero(ourhero, sometext):
    marqueeprint(sometext)
    print(lr_justify('[HERO]', '', 50))
    print(lr_justify(ourhero.name, '', 50))
    print(lr_justify(str('lvl: ' + str(ourhero.level)), '', 50))
    print(lr_justify(str('HP: ' + str(ourhero.hp) + '/' + str(ourhero.maxhp)), '', 50))
    print(lr_justify(str('XP: ' + str(ourhero.xp) + '/' + str(ourhero.nextlevel)), '', 50))


# if string is at least 80% similar, will return true
def similarstring(a, b):
    ourratio = SequenceMatcher(None, a, b).ratio()
    if debugging:
        print('correctness:' + str(ourratio))
    if ourratio >= .8:
        return True
    else:
        return False


if __name__ == '__main__':
    # Create all game databases (only needs to run once to make databases)

    firsttime = False
    if 'game.db' not in os.listdir('./db/'):
        centerprint('This looks like it\'s your first time playing.')
        centerprint('We must load the database first')
        centerprint('This will only take a couple of seconds...')
        firsttime = True

    debugging = input('Enter Debugging Mode?\n[1] for yes\nENTER for no\n')
    # re-creates the database, in case you change values1
    if firsttime == True:
        print('Loading Database:')
        oursetup = dbsetup.dbsetup()
        oursetup.setupdb()
    if debugging:
        printtest()
    # our database path
    dbpath = './db/game.db'
    # import and create our player database
    gamedb = connect(dbpath)
    conn = gamedb.cursor()
    gameloop()
