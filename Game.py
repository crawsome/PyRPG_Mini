import datetime
import os
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

suspensemode = 1


# TODO: Rewrite in full OOP, and separate / simplify get rid of spaghetti in Game.py


# adds a little suspense to offset the monotony of text input
def suspense():
    s = '.'
    if suspensemode:
        time.sleep(.2)



# One round of a battle
def battle():
    global ourHero
    global ourEnemy
    print('[ENEMY]')
    ourEnemy.printenemyinfo()
    suspense()
    ourHero.printheroinfo()
    suspense()
    print('|-------[ACTION]-------|')
    print('|   [a]tk    [d]ef     | \n|   [r]un    [i]tem    |\n| [h]eal coinflip 100g |')
    print('|----------------------|\n')
    nextmove = input('Action?\n')
    suspense()
    if ourHero.isalive():
        playerturn(nextmove)
    enemyturn()
    if not ourHero.isalive():
        ourHero.isbattling = False
        print('YOU DIED')
        quit()
    if not ourEnemy.isalive():
        ourHero.isbattling = False
        ourEnemy.reset()
        print('-------[VICTORY]--------')
        print('You gained ' + str(ourEnemy.xp) + ' Exp')
        print('You earned ' + str(ourEnemy.gold) + ' Gold')
        suspense()
        input('Press Enter to Continue\n')
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
    effatk = int(ourHero.atk + crit - ourEnemy.defn * .2)
    if effatk < 0:
        effatk = 0
    if m == 'a' or m == '':
        print('------[HERO ATTACK]------')
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
    if m == 'd':
        print('------[DEFENSE]------')
        ourHero.defn += ourHero.defn * .5
    if m == 'r':
        print('--------[RUN]--------')
        rand = random.randrange(0, 4)
        if rand == 0:
            print('you ran away')
            ourHero.isbattling = False
            return
        else:
            print('you can\'t run!')
    if m == 'i':
        pass
    if m == 'h':
        print('-------[HEAL]--------')
        print('\nDeath appears to flip a coin with you.\n')
        if ourHero.gold >=100:
            ourHero.gold -= 100
            newrand = random.randrange(0, 1)
            if newrand == 0:
                ourHero.hp = ourHero.maxhp
                print('\nHEAL SUCCESS\n' + ourHero.hp + '\n')
            else:
                print('\nHEAL FAILED\nYou lost the roll!\n')

        else:
            print('\nHEAL FAILED\nYou don\'t have enough money!\n')
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
            input('Press Enter to Continue\n')
        elif overunder == 1:
            ourEnemy.atk -= ourEnemy.atk * .2
            print(str(ourEnemy.name) + ' got Weaker!')
            input('Press Enter to Continue\n')
        elif overunder == 2:
            print(str(ourEnemy.name) + ' ran away!')
            ourEnemy.hp = 0
            ourHero.isbattling = False
            input('Press Enter to Continue\n')
            return
        if overunder in range(3, ourHero.dodge):
            print('\n-----[ENEMY ATTACK]-----')
            suspense()
            print(str(ourEnemy.name) + ' swings and misses!')
            print('\n------[END TURN]------\n')
            input('Press Enter to Continue\n')
            return
            suspense()
        if ourHero.isbattling:
            print('\n-----[ENEMY ATTACK]-----')
            suspense()
            effatk = int(ourEnemy.atk - (.2 * ourHero.defn))
            if effatk < 0:
                effatk = 0
            print('\n' + str(ourEnemy.name) + ' attacks ' + str(ourHero.name) + ' for ' + str(effatk) + ' damage!')
            ourarmor.dur -= int(effatk * .2)
            ourshield.dur -= int(effatk * .2)
            ourHero.hp = ourHero.hp - effatk
            print('\n------[END TURN]------\n')
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
    print('[w]arrior, [m]age, [h]unter')
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
    if ourHero.level >=15:
        print('MAX LEVEL! YOU WIN!\n THANKS FOR PLAYING')
    ourHero.printheroinfodetail()
    ourHero.level += 1
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


def camp():
    global ourHero
    ourHero.printheroinfo()
    print('you are now at camp')
    print('[r]est [i]tem [e]quip [h]ero [a]dventure [l]oad [s]ave [q]uit')
    m = input()
    if m == 'r':
        ourHero.hp = ourHero.maxhp
        ourHero.printheroinfo()
        return
    elif m == 'i':
        return
    elif m == 'e':
        inventory_management()
    elif m == 'h':
        ourHero.printheroinfodetail()
        ourweapon.printweaponinfo()
        ourshield.printshieldinfo()
        ourarmor.printarmorinfo()
    elif m == 'a':
        adventure()
    elif m == 'l':
        loadgame()
    elif m == 's':
        savegame()
    elif m == 'q':
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
    index = int(input("Which Character?\n"))
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
    heroname = input('Name your save file')
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
    print('[a]dventure or [c]amp')
    m = input()
    ourrand = random.randint(0, 100)
    suspense()
    if m == 'a' or m == '':
        if ourrand <= 80:
            ourHero.isbattling = True
            # Make new enemy
            ourEnemy = getenemy()
            print('--------[BATTLE]--------\n')
            # battle until one is dead
            turnnum = 1
            while ourHero.isalive() and ourEnemy.isalive() and ourHero.isbattling:
                print('--------[TURN ' + str(turnnum) + ']--------')
                battle()
                turnnum +=1
        elif 80 < ourrand <= 95:
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


if __name__ == '__main__':
    # this is for repopulating the database with modified CSV files
    # TODO: Make so database will not append if run more than once
    # Create all game databases (only needs to run once to make databases)
    dbsetup.setup()

    print('=================='
          '\nWelcome to MiniRPG\n'
          '==================')

    # our database path
    dbpath = './db/game.db'

    # import and create our player database
    gamedb = connect(dbpath)
    conn = gamedb.cursor()

    # Make new global hero and enemy which will change over time
    ourHero = newhero()

    print(ourHero.ourclass)

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

    ourHero.name = input('Please enter your name:\n')

    ourHero.heroperks()

    gameloop()
