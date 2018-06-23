import random

import Armor
import Game
import Item
import Shield
import Weapon
import dbsetup
from texttools import *


class Hero:
    def __init__(self, heroclass, herolevel, herohp, heroatk, herodefn, heronextlevel, herododge):
        # name
        self.name = ''

        # instance vars
        self.ourclass = heroclass
        self.level = herolevel
        self.nextlevel = heronextlevel

        # HP
        self.maxhp = herohp
        self.hp = self.maxhp

        # Attack
        self.baseatk = heroatk
        self.atk = self.baseatk

        # Defense
        self.basedef = herodefn
        self.defn = self.basedef

        # Dodge
        self.basedodge = herododge
        self.dodge = self.basedodge

        # Luck
        self.baseluck = 0
        self.luck = self.baseluck

        # Crit
        self.basecrit = 5
        self.crit = self.basecrit

        # game-created vars
        self.gold = 0
        self.xp = 0

        # Augmentations for hero classes
        self.hpaug = 0
        self.dodgeaug = 0
        self.defaug = 0
        self.atkaug = 0
        self.levelupaug = 0
        self.critaug = 0

        # Items container and usage
        self.items = []
        self.activeitem = 0

        # Gear container
        self.gear = []

        # Keep track of battle count
        self.battlecount = 0

        # Used for regen and haste potions
        self.regentimer = 0
        self.hastetimer = 0

        # A difficulty curve for determining lots of things
        self.atkcurve = 0
        self.defcurve = 0

        # equip objects
        self.ourweapon = Weapon.Weapon(0, 'training', 'wooden', 'stick', 3, 20, 'none')
        self.ourarmor = Armor.Armor(0, 'training', 'broken', 'plate', 2, 10)
        self.ourshield = Shield.Shield(0, 'training', 'wooden', 'ward', 3, 20)
        self.ouritem = Item.Item(0, 0, 0, 0, 0)
        self.isbattling = False

        # width of centered data in screencenter
        self.datawidth = 40

    # Heals user up to max health
    def heal(self, hpup):
        centerprint('You heal for ' + str(int(hpup)) + ' HP')
        print('')
        self.hp += hpup
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    # flip a coin, pay 100g, 1/2 chance of regaining health
    def healflip(self):
        marqueeprint('[HEAL FLIP]')
        centerprint('Death appears to flip a coin with you.')
        if self.gold >= 100:
            self.gold -= 100
            newrand = random.randrange(0, 1)
            if newrand == 0:
                self.heal(self.maxhp)
                marqueeprint('[HEAL SUCCESS]')
                centerprint(str(self.maxhp) + ' healed')
            else:
                marqueeprint('HEAL FAILED You lost the roll!')
        else:
            marqueeprint('[HEAL FAILED]')
            centerprint('You don\'t have enough money!')

    # sometimes you find food after a fight
    def food(self):
        hpback = int(self.maxhp * .2)
        centerprint('You found some food and healed ' + str(hpback) + ' HP.')
        self.heal(hpback)

    # take damage
    def damage(self, hpdown):
        effatk = hpdown + (hpdown * self.defcurve)
        self.hp -= int(effatk)
        centerprint(str(self.name) + ' takes ' + str(int(effatk)) + ' damage!')
        if self.hp < 0:
            self.hp = 0

    # kills the character
    def death(self):
        self.isbattling = False
        self.hp = 0
        marqueeprint('')
        marqueeprint('[GAME OVER]')
        marqueeprint('')
        print('')
        gridoutput(self.datadict())

    # adds XP to character, and levels up if it goes over
    def addxp(self, gainedxp):
        gainedxp = gainedxp + (gainedxp * self.defcurve)
        centerprint('You gained ' + str(int(gainedxp)) + ' Exp')
        self.xp += int(gainedxp)
        if self.xp >= self.nextlevel:
            self.levelup()

    # adds gold to character
    def addgold(self, gainedgold):
        gainedgold = gainedgold + (gainedgold * self.defcurve)
        centerprint('You gained ' + str(int(gainedgold + (gainedgold * self.defcurve))) + ' Gold')
        self.gold += int(gainedgold + (gainedgold * self.defcurve))

    # attempt to buy an item
    def buyitem(self, item):
        if self.canafford(item.val):
            self.gold -= item.val
            self.items.append(item)
            print('You bought ' + item.name)
        else:
            print('You can\'t afford that!')

    # see if you can afford an item
    def canafford(self, val):
        if self.gold >= val:
            return True
        else:
            return False

    # alive check
    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

    # applies hero's perks
    def heroperks(self):
        if self.ourclass == 'warrior':
            # more HP
            self.hpaug = 15
            # slower
            self.dodgeaug = 2
            # more def
            self.defaug = 12
            # low atk
            self.atkaug = 2
            # doofus is a slow leveler
            self.levelupaug = 1
            # mild crit chance boost
            self.critaug = 2
        elif self.ourclass == 'mage':
            # glass cannon
            self.hpaug = 5
            # med dodge
            self.dodgeaug = 5
            # low DEF
            self.defaug = 6
            # lower atk
            self.atkaug = 12
            # smarter, levels up quicker
            self.levelupaug = .6
            # mild crit chance boost
            self.critaug = 2
        elif self.ourclass == 'hunter':
            # med health
            self.hpaug = 10
            # high dodge
            self.dodgeaug = 8
            # med DEF
            self.defaug = 8
            # def ATK
            self.atkaug = 6
            # he gets by
            self.levelupaug = .8
            # high crit chance boost
            self.critaug = 6
        self.maxhp += self.hpaug
        self.hp += self.hpaug
        self.dodge += self.dodgeaug
        self.basedef += self.defaug
        self.defn += self.defaug
        self.nextlevel = int(self.nextlevel * self.levelupaug)
        self.baseatk += self.atkaug
        self.atk += self.atkaug

    # prints all hero stat info
    def printheroinfodetail(self):
        marqueeprint('[HERO DATA]')
        centerprint(Game.lr_justify('Class:', str(self.ourclass), self.datawidth))
        centerprint(Game.lr_justify('Name:', str(self.name), self.datawidth))
        centerprint(Game.lr_justify('Level:', str(self.level), self.datawidth))
        centerprint(Game.lr_justify('XP:', str(self.xp) + '/' + str(self.nextlevel), self.datawidth))
        centerprint(Game.lr_justify('HP:', str(self.hp) + '/' + str(self.maxhp), self.datawidth))
        centerprint(Game.lr_justify('Gold:', str(self.gold), self.datawidth))
        centerprint(Game.lr_justify('Atk:', str(self.atk), self.datawidth))
        centerprint(Game.lr_justify('Defense:', str(self.defn), self.datawidth))
        centerprint(Game.lr_justify('Dodge:', str(self.dodge), self.datawidth))
        centerprint(Game.lr_justify('battles fought', str(self.battlecount), self.datawidth))
        print('')

    # returns a dictionary of relevant user data for printing and delivering class information in a package
    def datadict(self):
        return {
            'Class': str(self.ourclass),
            'Name': str(self.name),
            'Level': str(self.level),
            'XP': str(str(self.xp) + '/' + str(self.nextlevel)),
            'HP': str(str(self.hp) + '/' + str(self.maxhp)),
            'Gold': str(self.gold),
            'Atk': str(self.atk),
            'Def': str(self.defn),
            'Dodge': str(self.dodge),
            'battles': str(self.battlecount)
        }

    # levels up hero
    def levelup(self):
        newdb = dbsetup.dbsetup()
        marqueeprint('[LEVEL UP]')
        self.xp -= self.nextlevel
        self.level += 1
        if self.level > 15:
            centerprint('MAX LEVEL! YOU WIN!')
            centerprint('THANKS FOR PLAYING')
            gridoutput(self.datadict())
            quit()
        newdb.conn.execute('SELECT * FROM levelnotes WHERE level = ' + str(self.level) + ';')
        rows = newdb.conn.fetchall()
        newdb.conn.close()
        new_hero_data = rows[0]
        self.maxhp = int(new_hero_data[1] + self.hpaug)
        self.hp = self.maxhp
        self.baseatk = int(new_hero_data[2] + self.atkaug)
        self.atk = self.baseatk
        self.basedef = int(new_hero_data[3] + self.defaug)
        self.defn = self.basedef
        self.nextlevel += int(new_hero_data[4] * self.levelupaug)
        self.dodge = int(new_hero_data[5] + self.dodgeaug)
        self.basecrit += self.critaug
        gridoutput(self.datadict())

    # fetches a new weapon for hero
    def newweapon(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM weapons WHERE "level" = ? AND "class" = ? ;',
                           (str(self.level), str(self.ourclass),))
        rows = newdb.conn.fetchall()
        newdb.conn.close()
        new_weapon_data = rows[0]
        ournewweapon = Weapon.Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3],
                                     new_weapon_data[4], new_weapon_data[5], new_weapon_data[6])
        return ournewweapon

    # fetches a new armor for hero
    def newarmor(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM armor WHERE "level" = ? AND "class" = ? ;',
                           (str(self.level), str(self.ourclass),))
        rows = newdb.conn.fetchall()
        newdb.conn.close()
        new_armor_data = rows[0]
        ournewarmor = Armor.Armor(new_armor_data[0], new_armor_data[1], new_armor_data[2], new_armor_data[3],
                                  new_armor_data[4], new_armor_data[5])
        return ournewarmor

    # fetches a new shield for hero
    def newshield(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM shields WHERE "level" = ? AND "class" = ? ;',
                           (str(self.level), str(self.ourclass),))
        rows = newdb.conn.fetchall()
        newdb.conn.close()
        new_shield_data = rows[0]
        ournewshield = Shield.Shield(new_shield_data[0], new_shield_data[1], new_shield_data[2], new_shield_data[3],
                                     new_shield_data[4], new_shield_data[5])
        return ournewshield

    # fetches a new item for hero
    def newitem(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM items WHERE "level" = ? ;', (self.level,))
        rows = newdb.conn.fetchall()
        newdb.conn.close()
        new_item_data = random.choice(rows)
        ournewitem = Item.Item(new_item_data[0], new_item_data[1], new_item_data[2], new_item_data[3], new_item_data[4])
        return ournewitem

    # re-equips all gear. Usually called when setting something like self.ourarmor = Armor.Armor(*args)
    def applyequip(self):
        self.atk = int(self.baseatk + self.ourweapon.baseatk)
        self.defn = int(self.basedef + self.ourarmor.defn + self.ourshield.defn)
