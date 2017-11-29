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


class Game:
    def __init__(self):
        # adds a little suspense
        self.suspensemode = 0

        # provides inner workings of game, some live-comments
        self.debugging = 0

        # provides a way to speed through battle (risky!)
        self.autoattack = 0

        # Create all game databases (only needs to run once to make databases)

        self.ourhero = 0
        self.ourenemy = 0

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
        self.dbpath = './db/game.db'
        # import and create our player database
        self.gamedb = connect(self.dbpath)
        self.conn = self.gamedb.cursor()

    # TODO: make self.ourhero.levelup and newhero the same function

    # makes a new hero object for when starting new game.
    def newhero(self):
        self.conn.execute('SELECT * FROM levelnotes WHERE level = 1;')
        rows = self.conn.fetchall()
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
        # hardest difficulty you defend the least, and attack the least
        if diff == '1' or diff == '':
            atkcurve = .2
            defcurve = .05
        elif diff == '2':
            atkcurve = .1
            defcurve = .1
        elif diff == '3':
            atkcurve = .05
            defcurve = .2
        else:
            centerprint('Please enter a valid selection')
            diff = 1
            atkcurve = .4
            defcurve = .05
            centerprint('Setting Difficulty to ' + str(diff))

        new_hero_data = rows[0]
        ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2],
                               new_hero_data[3], new_hero_data[4], new_hero_data[5])
        ournewhero.defcurve = defcurve
        ournewhero.atkcurve = atkcurve
        marqueeprint('ENTER NAME')
        centerprint('Your name, ' + str(ournewhero.ourclass) + '?\n')
        ournewhero.name = input()
        if ournewhero.name == '':
            ournewhero.name = 'Sir Lazy of Flabgard'
        return ournewhero

    # brings game back after death.
    def gameloop(self):
        while True:
            marqueeprint('')
            centerprint('MiniRPG')
            centerprint('Colin Burke 2017')
            marqueeprint('')
            centerprint('[n]ew game [l]oad')
            decision = input()

            if decision == 'n' or decision == '':
                # Make new global hero and enemy which will change over time
                self.ourhero = self.newhero()
                self.ourenemy = self.getenemy()

                self.ourhero.heroperks()
                self.ourhero.printheroinfodetail()
            if decision == 'l':
                print('lOADING GAME')
                self.ourhero = self.loadgame()
                self.ourenemy = self.getenemy()
            while self.ourhero.isalive():
                self.adventure()

    # where the meat of things happen, this decides what happens when you enter [a]dventure
    def adventure(self):
        centerprint('[a]dventure or [c]amp')
        m = input()
        ourrand = random.randint(0, 100)
        if m == 'a' or m == '':
            if ourrand <= 70:
                self.ourhero.isbattling = True
                # Make new enemy
                self.ourenemy = self.getenemy()
                marqueeprint('[BATTLE]')
                print('')
                # battle until one is dead
                turnnum = 1
                while self.ourhero.isalive() and self.ourenemy.isalive() and self.ourhero.isbattling:
                    marqueeprint('[TURN ' + str(turnnum) + ']')
                    self.battle()
                    turnnum += 1
            elif 70 < ourrand <= 90:
                marqueeprint('[FOUND ITEM!]')
                itemrand = random.randrange(0, 6)
                if itemrand == 0:
                    self.ourhero.ourarmor = self.ourhero.newarmor()
                    self.ourhero.ourarmor.printarmorinfo()
                elif itemrand == 1:
                    self.ourhero.ourweapon = self.ourhero.newweapon()
                    self.ourhero.ourweapon.printweaponinfo()
                elif itemrand == 2:
                    self.ourhero.ourshield = self.ourhero.newshield()
                    self.ourhero.ourshield.printshieldinfo()
                elif 3 <= itemrand <= 6:
                    self.ourhero.ouritem = self.ourhero.newitem()
                    self.ourhero.ouritem.printiteminfo()
                    self.ourhero.items.append(self.ourhero.ouritem)
                self.ourhero.applyequip()
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
                    xpgain = int(self.ourhero.nextlevel * .10)
                    self.ourhero.addxp(int(round(xpgain, 1)))
                if threechoicerandom == 1:
                    goldgain = int(self.ourhero.gold * .10)
                    self.ourhero.addgold(goldgain)
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
                ourriddle = self.getriddle()
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
                        if self.debugging:
                            print(answer + ', you cheater!')
                if similarstring(useranswer, answer) and useranswer != '':
                    centerprint('You have successfully answered the riddle')
                    centerprint('The answer was \"' + answer + '\"')
                    centerprint('I present you with this:')
                    self.ourhero.addgold(self.ourhero.level * 40)
                    self.ourhero.addxp(self.ourhero.nextlevel * .1)
                else:
                    centerprint('You Fail! Leave this place!')

        elif m == 'c':
            print('')
            self.camp()
        if not self.ourhero.isalive():
            return

    # One round of a battle
    def battle(self):
        self.ourhero.battlecount += 1
        self.printadversaries()
        print('')
        marqueeprint('[CHOOSE ACTION]')
        centerprint('[a]tk  [d]ef [r]un [i]tem')
        centerprint('Coinflip to [h]eal (100g)')
        centerprint('Action?')
        nextmove = input()
        # conditions to end battle
        if self.ourhero.isalive():
            turnnotused = True
            while turnnotused:
                turnnotused = self.playerturn(nextmove)
        if self.ourenemy.isalive():
            self.enemyturn()
        if not self.ourhero.isalive():
            self.ourhero.death()
            return
        if not self.ourenemy.isalive():
            self.ourhero.isbattling = False
            self.ourenemy.reset()
            marqueeprint('[VICTORY]')
            self.ourhero.addgold(self.ourenemy.gold + (self.ourenemy.gold * self.ourhero.defcurve))
            self.ourhero.addxp(self.ourenemy.xp + (self.ourenemy.xp * self.ourhero.defcurve))
            # 15% chance to get some health back.
            print('')
            if random.randrange(0, 100) in range(0, 15):
                self.ourhero.food()
        if not self.ourhero.isbattling:
            return
            wait = input()

    # One round of a player's turn
    def playerturn(self, m):
        turndecided = False
        self.ourhero.applyequip()
        marqueeprint('[HERO TURN]')
        crit = 0
        critrand = random.randrange(0, 100)
        if critrand in range(self.ourhero.crit, critrand):
            crit = self.ourhero.atk * .4
        effatk = int(self.ourhero.atk + crit)
        if effatk < 0:
            effatk = 0
        if m == 'a' or m == '':
            if critrand == 0:
                centerprint('CRITICAL HIT!')
            self.ourenemy.damage(effatk + crit, self.ourhero.atkcurve)
            self.ourhero.ourweapon.damagedur(effatk + crit, self.ourhero.defcurve)
            if self.ourenemy.hp < 0:
                self.ourenemy.hp = 0
                self.ourhero.isbattling = False
        elif m == 'd':
            marqueeprint('[DEFENSE]')
            self.ourhero.defn += self.ourhero.defn * self.ourhero.defcurve
        elif m == 'r':
            marqueeprint('[RUN ATTEMPT]')
            rand = random.randrange(0, 4)
            if rand == 0:
                centerprint('you ran away')
                self.ourhero.isbattling = False
                return
            else:
                centerprint('you can\'t run!')
        elif m == 'i':
            self.item_management()
        elif m == 'h':
            self.ourhero.healflip()
        wait = input()

        # for health regen potion
        if self.ourhero.regentimer > 0:
            regen = int(self.ourhero.hp * .2)
            self.ourhero.heal(regen)
            self.ourhero.regentimer -= 1

        # for haste potion for 5 turn dodge increases
        self.ourhero.dodge = self.ourhero.basedodge
        if self.ourhero.hastetimer > 0:
            self.ourhero.dodge = self.ourhero.basedodge + 5
            centerprint('Your dodge chance is elevated')
            self.ourhero.hastetimer -= 1
        else:
            self.ourhero.dodge = self.ourhero.basedodge

    # One round of an enemy turn
    def enemyturn(self):
        overunder = random.randrange(0, 20)
        if self.ourenemy.isalive:
            marqueeprint('[ENEMY ATTACK]')
            if overunder == 0:
                self.ourenemy.anger()
                wait = input()
            elif overunder == 1:
                self.ourenemy.weaker()
                wait = input()
            elif overunder == 2:
                centerprint(str(self.ourenemy.name) + ' ran away!')
                self.ourenemy.hp = 0
                self.ourhero.isbattling = False
                wait = input()
                return
            if overunder in range(3, self.ourhero.dodge):
                centerprint(str(self.ourenemy.name) + ' swings and misses!')
                wait = input()
                return
            if self.ourhero.isbattling:
                effatk = int(self.ourenemy.atk)
                if effatk < 0:
                    effatk = 0
                self.ourhero.ourarmor.damagedur(effatk, self.ourhero.defcurve)
                self.ourhero.ourshield.damagedur(effatk, self.ourhero.defcurve)
                self.ourhero.damage(effatk)
                wait = input()

    # fetch a random riddle from db
    def getriddle(self):
        self.conn.execute('SELECT * FROM riddles ORDER BY RANDOM() LIMIT 1' + ';')
        row = self.conn.fetchall()[0]
        riddle = [row[0], row[1]]
        return riddle
        pass

    # fetch a new enemy that is at hero's level (for now...)
    def getenemy(self):
        self.conn.execute('SELECT * FROM enemies WHERE level = ' + str(self.ourhero.level) + ';')
        rows = self.conn.fetchall()
        new_enemy = random.choice(rows)
        # create random enemy name
        levelname = random.choice((rows[0][1], rows[1][1], rows[2][1], rows[3][1], rows[4][1]))
        adjective = random.choice((rows[0][2], rows[1][2], rows[2][2], rows[3][2], rows[4][2]))
        enemyname = random.choice((rows[0][3], rows[1][3], rows[2][3], rows[3][3], rows[4][3]))
        ournewenemy = Enemy.Enemy(new_enemy[0], levelname, adjective, enemyname, new_enemy[4], new_enemy[5],
                                  (new_enemy[6] + (new_enemy[6] * self.ourhero.defcurve)), new_enemy[7], new_enemy[8],
                                  new_enemy[9])
        return ournewenemy

    # a blacksmith who can repair or sell gear
    def blacksmith(self):
        centerprint('An old Blacksmith rests at your camp')
        centerprint('He shows his wares and services:')
        centerprint('[f]ix gear [b]uy gear')
        nextdecision = input()
        centerprint('Gold: ' + str(self.ourhero.gold))
        if nextdecision == 'f':
            # offer equipment repair for any of the 3 slots, for 1g/durability point
            centerprint('The Blacksmith can offer repair ')
            centerprint('services for 1g/repair point')
            centerprint('Here is your gear durability:')
            data1 = ['Slot', 'Name', 'Dur', 'Broken?']
            data2 = [str(1), str(self.ourhero.ourweapon.name) + str(self.ourhero.ourweapon.type),
                     str(self.ourhero.ourweapon.dur) + '/' + str(self.ourhero.ourweapon.maxdur),
                     str(self.ourhero.ourweapon.isbroken())]
            data3 = [str(2), str(self.ourhero.ourshield.name) + ' ' + str(self.ourhero.ourshield.type),
                     str(self.ourhero.ourshield.dur) + '/' + str(self.ourhero.ourshield.maxdur),
                     str(self.ourhero.ourshield.isbroken())]
            data4 = [str(3), str(self.ourhero.ourarmor.name) + ' ' + str(self.ourhero.ourarmor.type),
                     str(self.ourhero.ourarmor.dur) + '/' + str(self.ourhero.ourarmor.maxdur),
                     str(self.ourhero.ourarmor.isbroken())]
            alldata = [data1, data2, data3, data4]
            fourrowprint(alldata, "Blacksmith")

            decision = input('What do you want to repair? [a] for all')
            if decision == '1' or decision == 'a':
                repaircost = self.ourhero.ourweapon.maxdur - self.ourhero.ourweapon.dur
                centerprint('Repair Your weapon?')
                centerprint('Cost: ' + str(repaircost) + ' gold')
                centerprint('[y]es [n]o')
                decision2 = input()
                if decision2 == 'y' and self.ourhero.gold >= repaircost:
                    self.ourhero.gold -= repaircost
                    self.ourhero.ourweapon.dur = self.ourhero.ourweapon.maxdur
                    centerprint('Repair Success.')
            if decision == '2' or decision == 'a':
                repaircost = self.ourhero.ourshield.maxdur - self.ourhero.ourshield.dur
                centerprint('Repair Your shield?')
                centerprint('Cost: ' + str(repaircost) + ' gold')
                centerprint('[y]es [n]o')
                decision2 = input()
                if decision2 == 'y' and self.ourhero.gold >= repaircost:
                    self.ourhero.gold -= repaircost
                    self.ourhero.ourshield.dur = self.ourhero.ourshield.maxdur
                    centerprint('Repair Success.')
            if decision == '3' or decision == 'a':
                repaircost = self.ourhero.ourarmor.maxdur - self.ourhero.ourarmor.dur
                centerprint('Repair Your armor?)')
                centerprint('Cost: ' + str(repaircost) + ' gold')
                centerprint('[y]es [n]o')
                decision2 = input()
                if decision2 == 'y' and self.ourhero.gold >= repaircost:
                    self.ourhero.gold -= repaircost
                    self.ourhero.ourarmor.dur = self.ourhero.ourarmor.maxdur
                    centerprint('Repair Success')
        # offer random choice of weapon, armor, or shield at 1.5x value price
        elif nextdecision == 'b':
            weaponforsale = self.ourhero.newweapon()
            armorforsale = self.ourhero.newarmor()
            shieldforsale = self.ourhero.newshield()
            marqueeprint('[YOUR GEAR]')
            leftprint(
                str(1) + ' \tName: ' + str(self.ourhero.ourweapon.name) + ' ' + str(
                    self.ourhero.ourweapon.type) + '\tAttack: ' + str(self.ourhero.ourweapon.atk) + '\tCost: ' + str(
                    self.ourhero.ourweapon.level * 50 * self.ourhero.defcurve))
            leftprint(
                str(2) + ' \tName: ' + str(self.ourhero.ourshield.name) + ' ' + str(
                    self.ourhero.ourshield.type) + '\tDefense: ' + str(self.ourhero.ourshield.defn) + '\tCost: ' + str(
                    self.ourhero.ourshield.level * 50 * self.ourhero.defcurve))
            leftprint(
                str(3) + ' \tName: ' + str(self.ourhero.ourarmor.name) + ' ' + str(
                    self.ourhero.ourarmor.type) + '\tDefense: ' + str(self.ourhero.ourarmor.defn) + '\tCost: ' + str(
                    self.ourhero.ourarmor.level * 50 * self.ourhero.defcurve))
            print('\n')
            # determine weapon coses
            wepcost = weaponforsale.level * 50 * self.ourhero.defcurve
            armcost = armorforsale.level * 50 * self.ourhero.defcurve
            shcost = shieldforsale.level * 50 * self.ourhero.defcurve
            marqueeprint('[GEAR FOR SALE]')
            leftprint(
                str(1) + ' \tName: ' + str(weaponforsale.name) + ' ' + str(weaponforsale.type) + '\tAttack: ' + str(
                    weaponforsale.atk) + '\tCost: ' + str(wepcost))
            leftprint(
                str(2) + ' \tName: ' + str(shieldforsale.name) + ' ' + str(shieldforsale.type) + '\tDefense: ' + str(
                    shieldforsale.defn) + '\tCost: ' + str(shcost))
            leftprint(
                str(3) + ' \tName: ' + str(armorforsale.name) + ' ' + str(armorforsale.type) + '\tDefense: ' + str(
                    armorforsale.defn) + '\tCost: ' + str(armcost))
            centerprint('Please enter decision')
            itemindex = input()
            if itemindex not in ['1', '2', '3']:
                centerprint('Please enter a valid choice')
            elif itemindex == '1':
                self.ourhero.ourweapon = weaponforsale
                if self.ourhero.gold < wepcost:
                    centerprint('You don\'t have enough money!')
                self.ourhero.gold -= wepcost
                centerprint('You equip your new gear: ' + str(weaponforsale.name) + ' ' + str(weaponforsale.type))
            elif itemindex == '2':
                self.ourhero.ourshield = shieldforsale
                if self.ourhero.gold < wepcost:
                    centerprint('You don\'t have enough money!')
                    return
                self.ourhero.gold -= armcost
                centerprint('You equip your new gear: ' + str(shieldforsale.name) + ' ' + str(shieldforsale.type))
            elif itemindex == '3':
                self.ourhero.ourarmor = armorforsale
                if self.ourhero.gold < shcost:
                    centerprint('You don\'t have enough money!')
                    return
                self.ourhero.gold -= shcost
                centerprint('You equip your new gear: ' + str(armorforsale.name) + ' ' + str(armorforsale.type))
            self.ourhero.applyequip()
            return

    # a camp where you regain hp after so many fights.
    def camp(self):
        self.ourhero.hp = self.ourhero.maxhp
        marqueeprint('[CAMP]')
        centerprint('You rest at camp. Hero HP: ' + str(self.ourhero.hp))
        centerprint('[a]dventure [i]tem [h]ero')
        centerprint('[p]eddler [b]lacksmith')
        centerprint('[l]oad [s]ave [q]uit')
        m = input()
        if m == 'i':
            marqueeprint('[ITEMS]')
            self.item_management()
            return
        elif m == 'h':
            marqueeprint('[HERO DETAIL]')
            self.ourhero.printheroinfodetail()
            wait = input()
            self.ourhero.ourweapon.printweaponinfo()
            wait = input()
            self.ourhero.ourshield.printshieldinfo()
            wait = input()
            self.ourhero.ourarmor.printarmorinfo()
            wait = input()
        elif m == 'a':
            return
            # adventure()
        elif m == 'l':
            marqueeprint('[LOADGAME]')
            self.ourhero = self.loadgame()
        elif m == 's':
            marqueeprint('[SAVEGAME]')
            self.savegame()
        elif m == 'b':
            marqueeprint('[BLACKSMITH]')
            self.blacksmith()
        elif m == 'p':
            marqueeprint('[PEDDLER\'S WARES]')
            self.peddler()
        elif m == 'q':
            marqueeprint('[QUIT]')
            decision = input('Are you sure?')
            if decision == 'y':
                quit()
        else:
            centerprint('You walk back to camp')

    # sell the hero items (will be able to buy soon)
    def peddler(self):
        centerprint('An old Peddler rests at your camp.')
        centerprint('He shows his wares:')
        centerprint('[b]uy, [s]ell, [f]ortune-telling')
        nextdecision = input()
        if nextdecision == 'b':
            pass
            item1 = self.ourhero.newitem()
            item2 = self.ourhero.newitem()
            item3 = self.ourhero.newitem()
            item4 = self.ourhero.newitem()
            item5 = self.ourhero.newitem()
            itemarray = [item1, item2, item3, item4, item5]
            for i, item in enumerate(itemarray):
                print(str(i + 1) + '\t' + item.name + '\t' + str(item.val * 1.5))
            print('Your selection? (ENTER to go back)')
            selection = input()
            if selection == '1':
                self.ourhero.buy(item1)
            elif selection == '2':
                self.ourhero.buy(item2)
            elif selection == '3':
                self.ourhero.buy(item3)
            elif selection == '4':
                self.ourhero.buy(item4)
            elif selection == '5':
                self.ourhero.buy(item5)
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
    def loadgame(self):
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
    def savegame(self):
        # pickle hero object to file
        # should prompt to overwrite
        heroname = input('Name your save file\nOr [c]ancel')
        if heroname == 'c':
            return
        savefolder = "./saves/"
        filepath = savefolder + heroname + '.hero'
        gamedata = self.ourhero
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
    def item_management(self):
        invlimit = 20
        marqueeprint('[CHOOSE ITEM]')
        if not self.ourhero.items:
            centerprint('Inventory Empty')
            return
        for i, item in enumerate(self.ourhero.items):
            print(str(i) + ' \tName: ' + str(item.name) + '\tEffect: ' + str(item.effect))
            if i > invlimit:
                break
        centerprint('Please enter decision')
        itemindex = input()
        try:
            itemindex = int(itemindex)
        except:
            itemindex = 0

        if itemindex not in range(0, invlimit):
            centerprint('Please enter a valid choice')
            return
        self.ourhero.ouritem = self.ourhero.items[int(itemindex)]
        self.ourhero.activeitem = self.ourhero.ouritem
        del (self.ourhero.items[int(itemindex)])
        centerprint('Using ' + str(self.ourhero.ouritem.name))
        if self.ourhero.ouritem.name == 'Healing Potion':
            self.healingpotion()
        if self.ourhero.ouritem.name == 'Explosive Mana Vial':
            if self.ourhero.isbattling:
                self.explosivemanavial()
            else:
                centerprint('You\'re not in battle!')
                return False
        if self.ourhero.ouritem.name == 'Health Regen Potion':
            self.healthregenpotion()
        if self.ourhero.ouritem.name == 'Haste Potion':
            self.hastepotion()
        if self.ourhero.ouritem.name == 'Weapon Repair Tincture':
            self.weaponrepairtincture()

    # hero uses a healing potion
    def healingpotion(self):
        marqueeprint('[HEALING POTION]')
        healed = self.ourhero.activeitem.effect
        self.ourhero.heal(healed)
        self.ourhero.activeitem = 0
        return

    # hero uses an item that damages enemy
    def explosivemanavial(self):
        marqueeprint('[EXPLOSIVE MANA BOMB]')
        centerprint('The Mana Vial EXPLODES!')
        dmg = self.ourhero.activeitem.effect
        self.ourenemy.damage(dmg, self.ourhero.atkcurve)
        self.ourhero.activeitem = 0
        return

    # adds health per turn
    def healthregenpotion(self):
        marqueeprint('[REGEN POTION]')
        self.ourhero.regentimer += 5
        centerprint(str(self.ourhero.regentimer) + ' turns health regen')
        self.ourhero.activeitem = 0

    # dodge buff
    def hastepotion(self):
        marqueeprint('[HASTE POTION]')
        centerprint(str(self.ourhero.hastetimer) + ' turns dodge buff')
        self.ourhero.hastetimer += 5
        self.ourhero.activeitem = 0

    # heals 60% of dur points to weapon
    def weaponrepairtincture(self):
        marqueeprint('[WEAPON REPAIR]')
        rep = self.ourhero.ourweapon.maxdur * .6
        centerprint('You repaired your weapon for ' + str(rep) + ' durability points')
        self.ourhero.ourweapon.dur += rep
        if self.ourhero.ourweapon.dur > self.ourhero.ourweapon.maxdur:
            self.ourhero.ourweapon.dur = self.ourhero.ourweapon.maxdur
        self.ourhero.activeitem = 0

    # adds a little suspense to offset the monotony of text input
    def suspense(self):
        s = ' '
        if self.suspensemode:
            time.sleep(.5)
            print(s)

    # Print hero and enemy justified on left and right
    def printadversaries(self):
        print(lr_justify('[HERO]', '[ENEMY]', 50))
        print(lr_justify(self.ourhero.name, self.ourenemy.name, 50))
        print(lr_justify(str('lvl: ' + str(self.ourhero.level)), str('lvl: ' + str(self.ourenemy.level)), 50))
        print(lr_justify(str('HP: ' + str(self.ourhero.hp) + '/' + str(self.ourhero.maxhp)),
                         str('HP: ' + str(self.ourenemy.hp) + '/' + str(self.ourenemy.maxhp)), 50))
        print(lr_justify(str('XP: ' + str(self.ourhero.xp) + '/' + str(self.ourhero.nextlevel)),
                         str('XP drop: ' + str(self.ourenemy.xp)),
                         50))

    # To be used on status screens
    def printmarqueehero(self, sometext):
        marqueeprint(sometext)
        print(lr_justify('[HERO]', '', 50))
        print(lr_justify(self.ourhero.name, '', 50))
        print(lr_justify(str('lvl: ' + str(self.ourhero.level)), '', 50))
        print(lr_justify(str('HP: ' + str(self.ourhero.hp) + '/' + str(self.ourhero.maxhp)), '', 50))
        print(lr_justify(str('XP: ' + str(self.ourhero.xp) + '/' + str(self.ourhero.nextlevel)), '', 50))


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
        # print(line)
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


# if string is at least 80% similar, will return true
def similarstring(a, b):
    ourratio = SequenceMatcher(None, a, b).ratio()
    if ourratio >= .8:
        return True
    else:
        return False
