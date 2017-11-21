import Game


class Weapon:
    # level,class,name,type,baseattack,durability,power
    def __init__(self, weaponlevel, weaponclass, weaponname, weapontype, weaponbaseatk, weapondur, weaponpower):
        self.level = weaponlevel
        self.ourclass = weaponclass
        self.type = weapontype
        self.name = weaponname
        self.baseatk = weaponbaseatk
        self.atk = self.baseatk
        self.maxdur = weapondur
        self.dur = self.maxdur
        self.power = weaponpower

    # damage durability, and check to see if broken
    def damagedur(self, aug, curve):
        self.dur -= int(aug * curve)
        self.isbroken()
        pass

    # restore dur and check to see if fixed
    def restoredur(self, aug):
        self.dur += aug
        if not self.isbroken():
            self.dur == self.maxdur

    def gearbreak(self):
        self.atk = int(self.baseatk * .3)

    # 15% durability = stat reduction
    def isbroken(self):
        if self.dur <= 0:
            self.gearbreak()
            return True
        elif self.dur >= self.maxdur * .15:
            return False

    def repair(self):
        self.atk = self.baseatk
        self.dur = self.maxdur

    def printweaponinfo(self):
        Game.marqueeprint('WEAPON')
        print(Game.lr_justify('Level:', str(self.level), 50))
        print(Game.lr_justify('Class:', str(self.ourclass), 50))
        print(Game.lr_justify('Name:', str(self.name), 50))
        print(Game.lr_justify('Type:', str(self.type), 50))
        print(Game.lr_justify('Atk:', str(self.atk) + '/' + str(self.baseatk), 50))
        print(Game.lr_justify('Dur:', str(self.dur) + '/' + str(self.maxdur), 50))
        print(Game.lr_justify('Broken?:', str(self.isbroken()), 50))
        print(Game.lr_justify('Power:', str(self.power), 50))
