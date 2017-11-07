class Weapon:
    # level,name,type,baseattack,durability,power
    def __init__(self, weaponlevel, weapontype, weaponbaseatk, weapondur, weaponpower):
        self.level = weaponlevel
        self.type = weapontype
        self.baseatk = weaponbaseatk
        self.atk = self.baseatk
        self.maxdur = weapondur
        self.dur = self.maxdur
        self.power = weaponpower

    def broken(self):
        self.baseatk = self.baseatk * .3

    def isbroken(self):
        if self.dur <= 0:
            return True
        else:
            return False

    def repair(self):
        self.atk = self.baseatk
        self.dur = self.maxdur

    def printweaponinfo(self):
        print('Weapon Data: ')
        print('\tLevel:\t\t' + str(self.level))
        print('\tType:\t' + str(self.type))
        print('\tBase Atk:\t\t' + str(self.baseatk))
        print('\tAtk:\t\t' + str(self.atk))
        print('\tMax Dur:\t\t\t' + str(self.maxdur))
        print('\tDur:\t\t\t' + str(self.dur))
        print('\tBroken?:\t\t' + str(self.isbroken()))
        print('\tPower:\t' + str(self.power))
