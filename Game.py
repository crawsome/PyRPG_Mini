import os
import random
from sqlite3 import connect

import Enemy
import Hero
import Armor
import Weapon
import Shield


# One round of a battle
def battle():
    ourHero.printheroinfo()

    print('[a]tk, [d]ef, [r]un\n')
    nextmove = input()
    playerturn(nextmove)
    enemyturn()
    if not ourHero.isalive():
        print('YOU DIED')
        quit()
    if not ourEnemy.isalive():
        ourEnemy.reset()
        print('VICTORY')
        print('You gained ' + str(ourEnemy.xp) + ' EXP')
        ourHero.xp += ourEnemy.xp
        if ourHero.xp > ourHero.nextlevel:
            ourHero.levelup()
        camp()
    pass


def playerturn(m):
    crit = 0
    critchance = random.randrange(0, 31)
    if critchance == 0:
        crit = ourHero.baseattack * .5
    effatk = int(round(ourHero.baseattack + crit - ourEnemy.defn, 1))
    if m == 'a':
        if critchance == 0:
            print('CRITICAL HIT!')
        print('Player attacks Enemy for ' + str(effatk))
        ourEnemy.hp = ourEnemy.hp - effatk
    if m == 'd':
        ourHero.defn += ourHero.defn * .2
    if m == 'r':
        rand = random.randrange(0, 4)
        if rand == 0:
            print('you ran away')
            camp()
        else:
            print('you can\'t run!')


def getenemy():
    conn.execute('SELECT * FROM enemies WHERE level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_enemy = random.choice(rows)
    # create random enemy name
    adjectives1 = random.choice((rows[0][2], rows[1][2], rows[2][2], rows[3][2], rows[4][2]))
    adjectives2 = random.choice((rows[0][3], rows[1][3], rows[2][3], rows[3][3], rows[4][3]))
    ourNewEnemy = Enemy.Enemy(new_enemy[0], adjectives1, adjectives2, new_enemy[3], new_enemy[4], new_enemy[5],
                              new_enemy[6], new_enemy[7], new_enemy[8], new_enemy[9])
    return ourNewEnemy


def newhero():
    conn.execute('SELECT * FROM levelnotes WHERE level = 1;')
    rows = conn.fetchall()
    print('[w]arrior, [m]age, [h]unter')
    ourclass = input()
    new_hero_data = rows[0]
    ournewhero = Hero.Hero(ourclass, new_hero_data[0], new_hero_data[1], new_hero_data[2], new_hero_data[3],
                           new_hero_data[4], [])
    return ournewhero


def newweapon():
    conn.execute('SELECT * FROM weapons where level = ' + str(ourHero.level) + ';')
    rows = conn.fetchall()
    new_weapon_data = rows[0]
    ournewweapon = Weapon.Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3], new_weapon_data[4])
    return ournewweapon
    # print(rows)


def newarmor():
    conn.execute('SELECT * FROM armor WHERE level = ' + str(ourHero.level) + ' AND WHERE classtype = ' + str(
        ourHero.ourclass) + ';')
    rows = conn.fetchall()
    new_armor_data = rows[0]
    ournewarmor = Armor.Armor(new_armor_data[0], new_armor_data[1], new_armor_data[2], new_armor_data[3], new_armor_data[4])
    return ournewarmor
    return


def newshield():
    conn.execute('SELECT * FROM shield WHERE level = ' + str(ourHero.level) + ' AND WHERE classtype = ' + str(
        ourHero.ourclass) + ';')
    rows = conn.fetchall()
    new_shield_data = rows[0]
    ournewshield = Shield.Shield(new_shield_data[0], new_shield_data[1], new_shield_data[2], new_shield_data[3], new_shield_data[4])
    return ournewshield
    return


def enemyturn():
    effatk = int(round(ourEnemy.atk - ourHero.defn, 1))
    if effatk < 0:
        effatk = 0
    print('\nEnemy Attacks Player for ' + str(effatk))
    ourHero.hp = ourHero.hp - effatk


def camp():
    ourHero.printheroinfo()
    print('you are now at camp')
    print('[r]est? [i]tem? [e]quip [a]dventure [l]oad [s]ave')
    m = input()
    if m == 'r':
        ourHero.hp = ourHero.maxhp
        pass
    elif m == 'i':
        pass
    elif m == 'e':
        inventory_management()
    elif m == 'a':
        adventure()
    elif m == 'l':
        inventory_management()
    elif m == 's':
        savegame()
    elif m == 'q':
        quit()


# pickle out to hero obj
def loadgame():
    pass


# pickle in to hero obj and start gameloop
def savegame():
    pass


def inventory_management():
    for i, item in enumerate(ourHero.heroitems):
        print('[' + i + '] - ' + item)
    pass


def gameloop():
    print('Welcome to MiniRPG\n\n')

    while True:
        adventure()


def adventure():
    print('[a]dventure or [c]amp')
    m = input()
    ourrand = random.randint(0, 100)
    if m == 'a':
        if ourrand <= 80:
            # Make new enemy
            ourEnemy = getenemy()
            print('\nYou are confronted by a ' + str(ourEnemy.name))
            # battle until one is dead
            ourEnemy.printenemyinfo()
            while ourHero.isalive() and ourEnemy.isalive():
                battle()
                os.system('cls')
        if 80 < ourrand <= 85:
            print('\nYou couldn\'t find anything so you came back to camp')
            camp()
        if 85 < ourrand <= 95:
            print('You found an item!')
            pass
        if 95 < ourrand <= 100:
            print('You find a traveler,')
            pass


# Create all game databases (only needs to run once to make databases)
# dbsetup.setup()

# our database path
dbpath = './db/game.db'

# import and create our player database
gamedb = connect(dbpath)
conn = gamedb.cursor()

# Make new global hero and enemy which will change over time
ourHero = newhero()

# new a basic weapon
newweapon()

ourEnemy = getenemy()

gameloop()
