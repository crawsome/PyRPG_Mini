class Armor:
    # level,classtype,name,type,basedef,durability
    def __init__(self, armorlevel, armortype, armorname, armorbasedef, armordur):
        self.level = armorlevel
        self.type = armortype
        self.name = armorname
        self.basedefn = armorbasedef
        self.defn = self.basedefn
        self.maxdur = armordur
        self.dur = self.maxdur

    def broken(self):
        self.basedefn = self.basedefn * .3

    def isbroken(self):
        if self.dur <= 0:
            return True
        else:
            return False

    def repair(self):
        self.defn = self.basedefn
        self.dur = self.maxdur

    def printarmorinfo(self):
        print('armor Data: ')
        print('\tLevel:\t\t' + str(self.level))
        print('\tType:\t' + str(self.type))
        print('\tBase Defense:\t\t' + str(self.basedefn))
        print('\tDefense:\t\t' + str(self.defn))
        print('\tMax Dur:\t\t\t' + str(self.maxdur))
        print('\tDur:\t\t\t' + str(self.dur))
        print('\tBroken?:\t\t' + str(self.isbroken()))
        print('\tPower:\t' + str(self.power))
