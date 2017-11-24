import random
import Armor
import Game
import Item
import Shield
import Weapon
import dbsetup


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
        self.diffcurve = .4
        self.enemydefhandicap = 0.5

        # equip objects
        self.ourweapon = Weapon.Weapon(0, 'training', 'wooden', 'stick', 3, 20, 'none')
        self.ourarmor = Armor.Armor(0, 'training', 'broken', 'plate', 2, 10)
        self.ourshield = Shield.Shield(0, 'training', 'wooden', 'ward', 3, 20)
        self.ouritem = Item.Item(0, 0, 0, 0, 0)

        self.isbattling = False

    def heal(self, hpup):
        self.hp += hpup
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def healflip(self):
        Game.marqueeprint('[HEAL FLIP]')
        Game.centerprint('Death appears to flip a coin with you.')
        if self.gold >= 100:
            self.gold -= 100
            newrand = random.randrange(0, 1)
            if newrand == 0:
                self.heal(self.maxhp)
                Game.marqueeprint('[HEAL SUCCESS]')
                Game.centerprint(str(self.maxhp) + ' healed')
            else:
                Game.marqueeprint('HEAL FAILED You lost the roll!')
        else:
            Game.marqueeprint('[HEAL FAILED]')
            Game.centerprint('You don\'t have enough money!')

    def food(self):
        hpback = int(self.maxhp * .2)
        Game.centerprint('You found some food. You gained')
        Game.centerprint(str(hpback) + ' HP back')
        self.heal(hpback)

    def damage(self, hpdown):
        self.hp -= hpdown
        if self.hp < self.maxhp:
            self.hp = 0

    def death(self):
        self.isbattling = False
        self.hp = 0
        Game.marqueeprint('')
        Game.marqueeprint(' YOU DIED ')
        Game.marqueeprint('')
        print('')
        self.printheroinfodetail()

    def addxp(self, gainedxp):
        Game.centerprint('You gained ' + str(int(gainedxp)) + ' Exp')
        self.xp += int(gainedxp)
        if self.xp >= self.nextlevel:
            self.levelup()

    def addgold(self, gainedgold):
        Game.centerprint('You earned ' + str(int(gainedgold + (gainedgold * self.diffcurve))) + ' Gold')
        self.gold += int(gainedgold + (gainedgold * self.diffcurve))

    def buy(self, item):
        if self.canafford(item.val):
            self.gold -= item.val
            self.items.append(item)
            print('You bought ' + item.name)
        else:
            print('You can\'t afford that!')

    def canafford(self, val):
        if self.gold >= val:
            return True
        else:
            return False

    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

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
            # regular leveling
            self.levelupaug = 1
        elif self.ourclass == 'mage':
            # glass cannon
            self.hpaug = 5
            # med dodge
            self.dodgeaug = 5
            # low DEF
            self.defaug = 6
            # lower atk
            self.atkaug = 12
            self.levelupaug = .6
        elif self.ourclass == 'hunter':
            self.hpaug = 10
            self.dodgeaug = 8
            self.defaug = 8
            self.atkaug = 6
            self.levelupaug = .8
        self.maxhp += self.hpaug
        self.hp += self.hpaug
        self.dodge += self.dodgeaug
        self.basedef += self.defaug
        self.defn += self.defaug
        self.nextlevel = int(self.nextlevel * self.levelupaug)
        self.baseatk += self.atkaug
        self.atk += self.atkaug

    def printheroinfodetail(self):
        Game.marqueeprint('[HERO DATA]')
        print(Game.lr_justify('Class:', str(self.ourclass), 50))
        print(Game.lr_justify('Name:', str(self.name), 50))
        print(Game.lr_justify('Level:', str(self.level), 50))
        print(Game.lr_justify('XP:', str(self.xp) + '/' + str(self.nextlevel), 50))
        print(Game.lr_justify('HP:', str(self.hp) + '/' + str(self.maxhp), 50))
        print(Game.lr_justify('Gold:', str(self.gold), 50))
        print(Game.lr_justify('Atk:', str(self.atk), 50))
        print(Game.lr_justify('Defense:', str(self.defn), 50))
        print(Game.lr_justify('Dodge:', str(self.dodge), 50))
        print(Game.lr_justify('battles fought', str(self.battlecount), 50))
        print('')

    def levelup(self):
        newdb = dbsetup.dbsetup()
        Game.marqueeprint('LEVEL UP!')
        print('\n')
        self.level += 1
        if self.level > 15:
            Game.marqueeprint('MAX LEVEL! YOU WIN!')
            Game.marqueeprint('THANKS FOR PLAYING')
            self.printheroinfodetail()
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
        self.xp = 0
        self.printheroinfodetail()

    def newweapon(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM weapons WHERE "level" = ? AND "class" = ? ;',(str(self.level), str(self.ourclass),))
        rows = newdb.conn.fetchall()
        newdb.conn.close()
        new_weapon_data = rows[0]
        ournewweapon = Weapon.Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3],
                                     new_weapon_data[4], new_weapon_data[5], new_weapon_data[6])
        return ournewweapon

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

    def newitem(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM items WHERE "level" = ? ;', (self.level,))
        rows = newdb.conn.fetchall()
        newdb.conn.close()
        new_item_data = random.choice(rows)
        ournewitem = Item.Item(new_item_data[0], new_item_data[1], new_item_data[2], new_item_data[3], new_item_data[4])
        return ournewitem

    def applyequip(self):
        self.atk = int(self.baseatk + self.ourweapon.baseatk)
        self.defn = int(self.basedef + self.ourarmor.defn + self.ourshield.defn)
