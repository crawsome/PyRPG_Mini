class Hero:
    def __init__(self, heroclass, herolevel, herohp, heroatk, herodefn, heronextlevel, herododge):
        self.ourclass = heroclass
        self.level = herolevel
        self.maxhp = herohp
        self.hp = self.maxhp
        self.baseatk = heroatk
        self.atk = self.baseatk
        self.basedef = herodefn
        self.defn = self.basedef
        self.nextlevel = heronextlevel
        self.gold = 0
        self.dodge = herododge
        self.items = [0, 0, 0, 0]
        self.xp = 0
        self.isbattling = False

    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

    def printheroinfo(self):
        print('Hero HP:\t' + str(self.hp))

    def printheroinfodetail(self):
        print('Hero Data: ')
        print('\tLevel:\t\t' + str(self.level))
        print('\tMax HP:\t\t' + str(self.maxhp))
        print('\tCurrent HP:\t' + str(self.hp))
        print('\tGold:\t\t' + str(self.gold))
        print('\tAtk:\t\t' + str(self.atk))
        print('\tDefense:\t' + str(self.defn))
        print('\tDodge:\t\t' + str(self.dodge))
        print('\tXP:\t\t\t' + str(self.xp))
        print('\tNextLvl:\t' + str(self.nextlevel))
