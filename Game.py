import os
import pickle
import random
from sqlite3 import connect
import time
import os
import datetime

from nonblock import *

import Armor
import Enemy
import Hero
import Item
import Shield
import Weapon
import dbsetup

foo = nonblock_read
foo.__init__()

suspensemode = 0


def suspense():
    sus = '..'
    if suspensemode:
        print(sus[0])
        time.sleep(.3)
        print(sus[1])
        time.sleep(.3)

# One round of a battle
def battle():
    global ourHero
    global ourEnemy
    ourHero.printheroinfo()
    print('[a]tk, [d]ef, [r]un')
    nextmove = input()

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
        print('VICTORY')
        print('You gained ' + str(ourEnemy.xp) + ' EXP')
        ourHero.xp += ourEnemy.xp
        ourHero.printheroinfodetail()
        if ourHero.xp > ourHero.nextlevel:
            levelup()
    if not ourHero.isbattling:
        return


def playerturn(m):

    global ourHero
    global ourEnemy
    crit = 0
    critchance = random.randrange(0, 31)
    if critchance == 0:
        crit = ourHero.atk * .4
    effatk = int(ourHero.atk + crit - ourEnemy.defn * .2)
    if effatk < 0:
        effatk = 0
    if m == 'a':
        if critchance == 0:
            print('CRITICAL HIT!')
        suspense()
        ourEnemy.hp = ourEnemy.hp - effatk
        if ourEnemy.hp < 0:
            ourEnemy.hp = 0
            ourHero.isbattling = False
        print('Player attacks Enemy for ' + str(effatk))
        ourEnemy.printenemyinfo()
    if m == 'd':
        ourHero.defn += ourHero.defn * .2
    if m == 'r':
        rand = random.randrange(0, 4)
        if rand == 0:

            print('you ran away')
            ourHero.isbattling = False
            return
        else:
            print('you can\'t run!')


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

    new_hero_data = rows[0]
    ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2], new_hero_data[3],
                           new_hero_data[4])
    return ournewhero


def levelup():
    print('LEVEL UP!\n ')
    ourHero.printheroinfodetail()
    ourHero.level += 1
    conn.execute('SELECT * FROM levelnotes WHERE level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_hero_data = rows[0]
    ourHero.maxhp = new_hero_data[1]
    ourHero.hp = ourHero.maxhp
    ourHero.atk += new_hero_data[2]
    ourHero.defn = new_hero_data[3]
    ourHero.nextlevel += new_hero_data[4]
    ourHero.printheroinfodetail()


def newweapon():
    conn.execute('SELECT * FROM weapons where level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_weapon_data = rows[0]
    ournewweapon = Weapon.Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3],
                                 new_weapon_data[4], new_weapon_data[5])
    return ournewweapon


def newarmor():
    conn.execute('SELECT * FROM armor WHERE "level" = ? AND "classtype" = ? ;',
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


def enemyturn():
    global ourHero
    if ourHero.isbattling:
        effatk = int(ourEnemy.atk - (.2 * ourHero.defn))
        if effatk < 0:
            effatk = 0
        suspense()
        print('\nEnemy Attacks Player for ' + str(effatk))
        ourHero.hp = ourHero.hp - effatk


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
    # load hero object from pickle file
    dirlist = os.listdir('./saves/')
    for i, item in enumerate(dirlist):
        print(str(i) + ' - ' + str(item))
        print(str(datetime.datetime.fromtimestamp(os.path.getmtime('./saves/' + item))))
        print('\n')
    index = int(input("Which Character?\n"))
    print(('./saves/%s', dirlist[0][index]))
    ourpickle = open(('./saves/' + str(dirlist[index])), "rb")
    ourHero = pickle.load(ourpickle)[0]
    # assign this hero object to be the object
    # start the game loop with the loaded hero


# pickle in to hero obj and start gameloop
def savegame():
    # pickle hero object to file
    # should prompt to overwrite
    heroname = input('Name your save file')
    savefolder = "./saves/"
    filepath = savefolder + heroname + '.hero'
    if not os.path.isfile(filepath):
        with open(filepath, 'wb') as f:
            pickle.dump([ourHero], f, -1)
    else:
        answer = input('Overwrite?')
        if answer.lower() == 'y':
            with open(filepath, 'wb') as f:
                pickle.dump([ourHero], f, -1)
        elif answer.lower() == 'n':
            newname = input('Enter New Save file name')
            with open(filepath + str(newname), 'wb') as f:
                pickle.dump([ourHero], f, -1)


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
    if m == 'a':
        if ourrand <= 80:
            ourHero.isbattling = True
            # Make new enemy
            ourEnemy = getenemy()
            print('\nA Lvl ' + str(ourEnemy.level) + ' ' + str(ourEnemy.name) + ' blocks your path!')
            # battle until one is dead
            ourEnemy.printenemyinfo()
            while ourHero.isalive() and ourEnemy.isalive() and ourHero.isbattling:
                battle()
        elif 80 < ourrand <= 95:
            print('You found and equipped a ')
            itemrand = random.randrange(0, 3)
            if itemrand == 0:
                ourarmor = newarmor()
                ourarmor.printarmorinfo()
            elif itemrand == 1:
                ourweapon = newweapon()
                ourweapon.printweaponinfo()
            elif itemrand == 2:
                ourshield = newshield()
                ourshield.printshieldinfo()
            elif itemrand == 3:
                ouritem = newitem()
                ouritem.printiteminfo()
            applyequip()
        elif 95 < ourrand <= 100:
            print('You find a traveler,')
            print('He says:,')
            with open('./quoteslist.txt', 'rb') as f:
                quotelist = f.read().splitlines()
                quote = random.choice(quotelist)
                quote = quote.decode('utf-8')
                print(quote)
            print('You venture back to camp')
            pass
    elif m == 'c':
        camp()


if __name__ == '__main__':
    # Create all game databases (only needs to run once to make databases)
    # dbsetup.setup()

    print('=================='
          '\nWelcome to MiniRPG\n'
          '==================')

    # our database path
    dbpath = './db/game.db'

    # import and create our player database
    gamedb = connect(dbpath)
    conn = gamedb.cursor()

    # this is for repopulating the database with modified CSV files
    # TODO: Make so database will not append if run more than once
    # dbsetup.setup()

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

    gameloop()
