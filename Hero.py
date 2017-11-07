import math


class Hero:
    #Level,HP,ATK,DEF,xptonextlevel
    def __init__(self, heroclass, herolevel, herohp, heroatk, herodefn, heronextlevel, heroitems):
        self.ourclass = heroclass
        self.level = herolevel
        self.maxhp = herohp
        self.hp = self.maxhp
        self.atk = heroatk
        self.defn = herodefn
        self.nextlevel = heronextlevel
        self.items = heroitems
        self.xp = 0
        self.ourclass = 'm'

        self.ourweapon = heroitems[0]
        self.weaponlevel = 1
        self.weaponname = 'Novice Sword'
        self.weapondmg = 8
        self.weapontype = 'Sword'
        self.baseattack = self.weapondmg + self.weapondmg
        self.durability = 40
        self.power = 'none'

        self.ourarmor = self.items[1]

        self.ourshield = self.items[2]

        self.item = self.items[3]


    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False


    def levelup(self):
        print('LEVEL UP!')
        self.printheroinfo()
        self.level += 1
        self.maxhp = self.maxhp + math.ceil(self.maxhp * .14)
        self.atk = self.atk + self.atk * .2
        self.atk = self.atk + self.atk * .2
        self.nextlevel += math.ceil(self.nextlevel * 2.2)


    def printheroinfo(self):
        print('Hero Data: ')
        print('\tMax HP:\t\t' + str(self.maxhp))
        print('\tCurrent HP:\t' + str(self.hp))
        print('\tAtk:\t\t' + str(self.atk))
        print('\tXP:\t\t\t' + str(self.xp))
        print('\tNextLvl:\t' + str(self.nextlevel))
