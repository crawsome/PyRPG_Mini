class Armor:
    # level,classtype,name,type,basedef,durability
    def __init__(self, armorlevel, armorclasstype, armorname, armortype, armorbasedef, armordur):
        self.level = armorlevel
        self.classtype = armorclasstype
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
        print('Armor: ')
        print('\tLevel:\t\t\t' + str(self.level))
        print('\tName:\t\t\t' + str(self.name))
        print('\tType:\t\t\t' + str(self.type))
        print('\tBase Defense:\t' + str(self.basedefn))
        print('\tDefense:\t\t' + str(self.defn))
        print('\tMax Dur:\t\t' + str(self.maxdur))
        print('\tDur:\t\t\t' + str(self.dur))
        print('\tBroken?:\t\t' + str(self.isbroken()))
