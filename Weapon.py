from texttools import *


class Weapon:
    # level,class,name,type,baseattack,durability,power
    def __init__(self, weaponlevel, weaponclass, weaponname, weapontype, weaponbaseatk, weapondur, weaponpower):
        # Weapon level
        self.level = weaponlevel

        # Weapon hero class type
        self.ourclass = weaponclass

        # Weapon type
        self.type = weapontype

        # Weapon Name
        self.name = weaponname

        # Weapon atk
        self.baseatk = weaponbaseatk
        self.atk = self.baseatk

        # Weapon durability
        self.maxdur = weapondur
        self.dur = self.maxdur

        # Weapon Power (Not implemented yet)
        self.power = weaponpower

    # damage durability, and check to see if broken
    def damagedur(self, aug, curve):
        self.dur -= int(aug * curve * .1)
        self.isbroken()
        pass

    # restore dur by integer and check to see if fixed
    def restoredur(self, aug):
        self.dur += aug
        if not self.isbroken():
            self.dur == self.maxdur
            self.atk = self.baseatk

    # restore dur entirely
    def repair(self):
        self.atk = self.baseatk
        self.dur = self.maxdur

    # this breaks the gear
    def gearbreak(self):
        self.atk = int(self.baseatk * .3)

    # 15% durability = stat reduction
    def isbroken(self):
        if self.dur <= 0:
            self.gearbreak()
            return True
        elif self.dur >= self.maxdur * .15:
            return False

    # prints all weapon stats
    def printweaponinfo(self):
        marqueeprint('WEAPON')
        print(lr_justify('Level:', str(self.level), 70))
        print(lr_justify('Class:', str(self.ourclass), 70))
        print(lr_justify('Name:', str(self.name), 70))
        print(lr_justify('Type:', str(self.type), 70))
        print(lr_justify('Atk:', str(self.atk) + '/' + str(self.baseatk), 70))
        print(lr_justify('Dur:', str(self.dur) + '/' + str(self.maxdur), 70))
        print(lr_justify('Broken?:', str(self.isbroken()), 70))
        print(lr_justify('Power:', str(self.power), 70))

    # ['Level', 'Name', 'Type', 'Atk', 'Dur', 'Broken?', 'Power']
    def datadict(self):

        return {'Level': str(self.level),
                'Name': (str(self.name) + ' ' + str(self.type)),
                'Atk': str(self.atk),
                'Dur': (str(self.dur) + '/' + str(self.maxdur)),
                'Broken?': str(self.isbroken()),
                'Repair Cost': str(self.maxdur - self.dur) + ' gold',
                'Power': str(self.power)
                }
