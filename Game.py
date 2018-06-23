import datetime
import os
import pickle
import random
import time
from sqlite3 import connect
import Enemy
import Hero
import dbsetup
from texttools import *


# game class makes the game work instantiates all other classes at some point.
class Game:
    def __init__(self):
        # adds a little suspense
        # TODO: add suspense option to some printing methods?
        self.suspensemode = 0

        # provides inner workings of game, some live-comments
        # TODO: add more comments and stats as game goes on
        self.debugging = 0
        centerprint('Debugging Mode? [1] for yes, [ENTER] for no')
        self.debugging = input()

        # riddle mode 0 - optional, 1 - mandatory
        centerprint('Riddles Mandatory? [1] for yes, [ENTER] for no')
        self.riddlemode = input()
        if self.riddlemode == '':
            self.riddlemode = 0

        # provides a way to speed through battle (risky!)
        self.autoattack = 0

        # make blank hero and enemy objects
        self.ourhero = 0
        self.ourenemy = 0

        # global text width
        self.textwidth = 70

        # width of data, so it's not so spaced-out
        self.datawidth = 55

        # Create all game databases (only needs to run once to make databases)
        firsttime = False
        if 'game.db' not in os.listdir('./db/'):
            centerprint('This looks like it\'s your first time playing.')
            centerprint('We must load the database first')
            centerprint('This will only take a moment...')
            firsttime = True

        # re-creates the database, in case you change values1
        if firsttime:
            print('Loading Database:')
            oursetup = dbsetup.dbsetup()
            oursetup.setupdb()
        if self.debugging:
            printtest()

        # our database path
        self.dbpath = './db/game.db'

        # import and create our player database
        self.gamedb = connect(self.dbpath)
        self.conn = self.gamedb.cursor()

        # width of centered data in screencenter
        self.datawidth = 55

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

        # the harder the difficulty, the less your attack and defense
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
        ournewhero = Hero.Hero(ourclass,
                               new_hero_data[0], new_hero_data[1],
                               new_hero_data[2], new_hero_data[3],
                               new_hero_data[4], new_hero_data[5])
        ournewhero.defcurve = defcurve
        ournewhero.atkcurve = atkcurve
        marqueeprint('[ENTER NAME]')
        centerprint('Your name, ' + str(ournewhero.ourclass) + '?\n')
        ournewhero.name = input()
        if ournewhero.name == '':
            ournewhero.name = 'Sir Lazy'
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
                gridoutput(self.ourhero.datadict())
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
                # battle until one is dead
                turnnum = 1
                while self.ourhero.isalive() and self.ourenemy.isalive() and self.ourhero.isbattling:
                    marqueeprint('[TURN ' + str(turnnum) + ']')
                    self.battle()
                    turnnum += 1
            elif 70 < ourrand <= 90:
                marqueeprint('[FOUND ITEM]')
                itemrand = random.randrange(0, 6)
                if itemrand == 0:
                    self.ourhero.ourarmor = self.ourhero.newarmor()
                    gridoutput(self.ourhero.ourarmor.datadict())
                elif itemrand == 1:
                    self.ourhero.ourweapon = self.ourhero.newweapon()
                    gridoutput(self.ourhero.ourweapon.datadict())
                elif itemrand == 2:
                    self.ourhero.ourshield = self.ourhero.newshield()
                    gridoutput(self.ourhero.ourshield.datadict())
                elif 3 <= itemrand <= 6:
                    self.ourhero.ouritem = self.ourhero.newitem()
                    gridoutput(self.ourhero.ouritem.datadict())
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
                    wrapstring = textwrap.wrap(quote, width=self.datawidth)
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
                centerprint('You find nothing and wander back to camp')
                pass
            elif 95 < ourrand <= 100:
                self.riddle()
        elif m == 'c':
            self.camp()
        if not self.ourhero.isalive():
            return

    # One round of a battle
    def battle(self):
        self.ourhero.battlecount += 1
        self.printadversaries(self.datawidth)
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
                #wait = input()
        if self.ourenemy.isalive():
            self.enemyturn()
            #wait = input()
        if not self.ourhero.isalive():
            self.ourhero.death()
            #wait = input()
            return
        if not self.ourenemy.isalive():
            self.ourhero.isbattling = False
            self.ourenemy.reset()
            marqueeprint('[VICTORY]')
            self.ourhero.addgold(self.ourenemy.gold + (self.ourenemy.gold * self.ourhero.defcurve))
            self.ourhero.addxp(self.ourenemy.xp + (self.ourenemy.xp * self.ourhero.defcurve))
            # 15% chance to get some health back.
            if random.randrange(0, 100) in range(0, 15):
                self.ourhero.food()
            centerprint('Press [Enter] To continue')
            wait = input()
        if not self.ourhero.isbattling:
            return

    # One round of a player's turn
    def playerturn(self, m):
        # for health regen potion
        if self.ourhero.regentimer > 0:
            regen = int(self.ourhero.maxhp * .2)
            self.ourhero.heal(regen)
            self.ourhero.regentimer -= 1
        # for haste potion for 5 turn dodge increases
        self.ourhero.dodge = self.ourhero.basedodge
        if self.ourhero.hastetimer > 0:
            centerprint('Your dodge chance is elevated')
            self.ourhero.hastetimer -= 1
        else:
            self.ourhero.dodge = self.ourhero.basedodge
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
            return False
        elif m == 'd':
            marqueeprint('[DEFENSE]')
            self.ourhero.defn += self.ourhero.defn * self.ourhero.defcurve
            return False
        elif m == 'r':
            marqueeprint('[RUN ATTEMPT]')
            rand = random.randrange(0, 4)
            if rand == 0:
                centerprint('you ran away')
                self.ourhero.isbattling = False
            else:
                centerprint('you can\'t run!')
            return False
        elif m == 'i':
            itemnotchosen = True
            while itemnotchosen:
                itemnotchosen = self.item_management()
            return False
        elif m == 'h':
            self.ourhero.healflip()
        wait = input()

    # One round of an enemy turn
    def enemyturn(self):
        overunder = random.randrange(0, 20)
        if self.ourenemy.isalive:
            marqueeprint('[ENEMY ATTACK]')
            if overunder == 0:
                self.ourenemy.anger()
            elif overunder == 1:
                self.ourenemy.weaker()
            elif overunder == 2:
                centerprint(str(self.ourenemy.name) + ' ran away!')
                self.ourenemy.hp = 0
                self.ourhero.isbattling = False
                return
            if overunder in range(3, self.ourhero.dodge):
                centerprint(str(self.ourenemy.name) + ' swings and misses!')
                return
            if self.ourhero.isbattling:
                effatk = int(self.ourenemy.atk)
                if effatk < 0:
                    effatk = 0
                self.ourhero.ourarmor.damagedur(effatk, self.ourhero.defcurve)
                self.ourhero.ourshield.damagedur(effatk, self.ourhero.defcurve)
                self.ourhero.damage(effatk)

    def riddle(self):
        marqueeprint('[RIDDLE]')
        centerprint('The area gets quiet. The wind blows.')
        centerprint('A torn page lands in your grasp. It reads:')
        print('\n')
        # query database for a single random riddle
        self.conn.execute('SELECT * FROM riddles ORDER BY RANDOM() LIMIT 1' + ';')
        row = self.conn.fetchall()[0]
        ourriddle = [row[0], row[1]]
        wrapstring = textwrap.wrap(ourriddle[0], width=self.datawidth)
        answer = str(ourriddle[1]).lower()
        for line in wrapstring:
            centerprint(line)
        centerprint('Speak the answer to the wind...')
        useranswer = input()
        if useranswer == '' and self.riddlemode == 1:
            while useranswer == '':
                centerprint('Please answer the riddle.')
                useranswer = input()
                if self.debugging:
                    marqueeprint(answer + ', you cheater!')
        if similarstring(useranswer, answer) and useranswer != '':
            centerprint('You have successfully answered the riddle')
            centerprint('The answer was \"' + answer + '\"')
            centerprint('I present you with this:')
            self.ourhero.addgold(self.ourhero.level * 44)
            self.ourhero.addxp(self.ourhero.nextlevel * .17)
        else:
            centerprint('You Fail! Leave this place!')


    # fetch a new enemy that is at hero's level (for now...)
    def getenemy(self):
        self.conn.execute('SELECT * FROM enemies WHERE level = ' + str(self.ourhero.level) + ';')
        rows = self.conn.fetchall()
        new_enemy = random.choice(rows)

        # create random enemy name
        levelname = random.choice((rows[0][1], rows[1][1],
                                   rows[2][1], rows[3][1],
                                   rows[4][1]))
        # part of random name
        adjective = random.choice((rows[0][2], rows[1][2],
                                   rows[2][2], rows[3][2],
                                   rows[4][2]))
        # part of random name
        enemyname = random.choice((rows[0][3], rows[1][3],
                                   rows[2][3], rows[3][3],
                                   rows[4][3]))
        # part of random name
        ournewenemy = Enemy.Enemy(new_enemy[0], levelname, adjective, enemyname, new_enemy[4],
                                  new_enemy[5], (new_enemy[6] + (new_enemy[6] * self.ourhero.defcurve)),
                                  new_enemy[7], new_enemy[8], new_enemy[9])
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

            # print all your gear out
            gridoutput(self.ourhero.ourweapon.datadict())
            gridoutput(self.ourhero.ourshield.datadict())
            gridoutput(self.ourhero.ourarmor.datadict())

            # user input for what to repair, or all of it, for convenience
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
            gridoutput(self.ourhero.ourweapon.datadict())
            gridoutput(self.ourhero.ourshield.datadict())
            gridoutput(self.ourhero.ourarmor.datadict())
            print('')

            # determine weapon costs
            wepcost = weaponforsale.level * 60 * self.ourhero.defcurve
            armcost = armorforsale.level * 60 * self.ourhero.defcurve
            shcost = shieldforsale.level * 60 * self.ourhero.defcurve

            data1 = [str(weaponforsale.name), str(weaponforsale.type),
                     str(weaponforsale.baseatk),
                     str(wepcost)]
            data2 = [str(shieldforsale.name), str(shieldforsale.type),
                     str(shieldforsale.basedefn),
                     str(shcost)]
            data3 = [str(armorforsale.name), str(armorforsale.type),
                     str(armorforsale.basedefn),
                     str(armcost)]

            title = ('[GEAR FOR SALE]')
            dataheader = ['Name', 'Type', 'Atk/Def', 'Cost']
            alldata = [data1, data2, data3]
            fiverowprintoptions(dataheader, alldata, title)
            print('\n')
            centerprint('Please enter decision [ENTER] to go back')
            itemindex = input()
            if itemindex not in ['1', '2', '3', '']:
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
        camping = True
        while camping:
            self.ourhero.hp = self.ourhero.maxhp
            marqueeprint('[CAMP]')
            centerprint('You rest at camp. Hero HP: ' + str(self.ourhero.hp))
            centerprint('[a]dventure [i]tem [h]ero')
            centerprint('[p]eddler [b]lacksmith')
            centerprint('[l]oad [s]ave [q]uit')
            m = input()
            if m == 'i':
                iteming = True
                while iteming:
                    iteming = self.item_management()
            elif m == 'h':
                marqueeprint('[HERO DETAIL]')
                gridoutput(self.ourhero.datadict())
                wait = input()
                gridoutput(self.ourhero.ourweapon.datadict())
                wait = input()
                gridoutput(self.ourhero.ourshield.datadict())
                wait = input()
                gridoutput(self.ourhero.ourarmor.datadict())
                wait = input()
            elif m == 'a' or m == '':
                return
                # adventure()
            elif m == 'l':
                marqueeprint('[LOAD GAME]')
                self.ourhero = self.loadgame()
            elif m == 's':
                marqueeprint('[SAVE GAME]')
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
        centerprint('[b]uy, [r]iddle (100g)')
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
                self.ourhero.buyitem(item1)
            elif selection == '2':
                self.ourhero.buyitem(item2)
            elif selection == '3':
                self.ourhero.buyitem(item3)
            elif selection == '4':
                self.ourhero.buyitem(item4)
            elif selection == '5':
                self.ourhero.buyitem(item5)
            elif selection == '':
                centerprint('\"WHYD YOU COME HERE AND NOT BUY ANYTHING?\"')
                return
            else:
                centerprint('Get out of here you bum!')
                # offer random choice of items at 1.5x value price
        if nextdecision == 'r':
            if self.ourhero.canafford(100):
                self.ourhero.gold -= 100
                self.riddle()

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
        if not self.ourhero.items:
            centerprint('Inventory Empty')
            return False
        # print all the item's info
        for i, item in enumerate(self.ourhero.items):
            leftprint('ITEM: ' + str(i+1))
            gridoutput(self.ourhero.items[i].datadict())
        centerprint('Please enter decision, [ENTER] to go back')
        try:
            itemindex = input()
            itemindex = int(itemindex)
            itemindex -= 1
            self.ourhero.ouritem = self.ourhero.items[int(itemindex)]
            del (self.ourhero.items[int(itemindex)])
        except ValueError:
            centerprint('Please enter a valid choice')
            return False
        except IndexError:
            centerprint('Please enter a valid choice')
            return False
        self.ourhero.activeitem = self.ourhero.ouritem
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


    # hero uses an item that damages enemy
    def explosivemanavial(self):
        marqueeprint('[EXPLOSIVE MANA BOMB]')
        centerprint('The Mana Vial EXPLODES!')
        dmg = self.ourhero.activeitem.effect
        self.ourenemy.damage(dmg, self.ourhero.atkcurve)
        self.ourhero.activeitem = 0


    # adds health per turn
    def healthregenpotion(self):
        marqueeprint('[REGEN POTION]')
        self.ourhero.regentimer += 5
        centerprint(str(self.ourhero.regentimer) + ' turns health regen')
        self.ourhero.activeitem = 0

    # dodge buff
    def hastepotion(self):
        marqueeprint('[HASTE POTION]')
        self.ourhero.hastetimer += 5
        centerprint(str(self.ourhero.hastetimer) + ' turns dodge buff')
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
    def printadversaries(self, datawidth):
        self.textwidth = datawidth
        centerprint(lr_justify('[HERO]', '[ENEMY]', self.textwidth))
        centerprint(lr_justify(self.ourhero.name, self.ourenemy.name, self.textwidth))
        centerprint(lr_justify(str('lvl: ' + str(self.ourhero.level)),
                               str('lvl: ' + str(self.ourenemy.level)),self.textwidth))
        centerprint(lr_justify(str('HP: ' + str(self.ourhero.hp) + '/' + str(self.ourhero.maxhp)),
                         str('HP: ' + str(self.ourenemy.hp) + '/' + str(self.ourenemy.maxhp)), self.textwidth))
        centerprint(lr_justify(str('XP: ' + str(self.ourhero.xp) + '/' + str(self.ourhero.nextlevel)),
                         str('XP drop: ' + str(self.ourenemy.xp)),self.textwidth))

    # To be used on status screens
    def printmarqueehero(self, sometext):
        marqueeprint(sometext)
        print(lr_justify('[HERO]', '', self.textwidth))
        print(lr_justify(self.ourhero.name, '', self.textwidth))
        print(lr_justify(str('lvl: ' + str(self.ourhero.level)), '', self.textwidth))
        print(lr_justify(str('HP: ' + str(self.ourhero.hp) + '/' + str(self.ourhero.maxhp)), '', self.textwidth))
        print(lr_justify(str('XP: ' + str(self.ourhero.xp) + '/' + str(self.ourhero.nextlevel)), '', self.textwidth))
