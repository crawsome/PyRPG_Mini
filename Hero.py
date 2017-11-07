import math


class Hero:
    # Level,HP,ATK,DEF,xptonextlevel
    def __init__(self, heroclass, herolevel, herohp, heroatk, herodefn, heronextlevel):
        self.ourclass = heroclass
        self.level = herolevel
        self.maxhp = herohp
        self.hp = self.maxhp
        self.atk = heroatk
        self.defn = herodefn
        self.nextlevel = heronextlevel
        self.items = [0, 0, 0, 0]
        self.xp = 0

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
        self.nextlevel += math.ceil(self.nextlevel * 1.8)

    def printheroinfo(self):
        print('\tCurrent HP:\t' + str(self.hp))

    def printheroinfodetail(self):
        print('Hero Data: ')
        print('\tMax HP:\t\t' + str(self.maxhp))
        print('\tCurrent HP:\t' + str(self.hp))
        print('\tAtk:\t\t' + str(self.atk))
        print('\tXP:\t\t\t' + str(self.xp))
        print('\tNextLvl:\t' + str(self.nextlevel))
