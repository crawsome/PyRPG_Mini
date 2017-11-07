class Shield:
    # level,class,name,type,basedef,durability
    def __init__(self, shieldlevel, shieldclass, shieldname, shieldtype, shieldbasedefn, shielddur):
        self.level = shieldlevel
        self.ourshieldclass = shieldclass
        self.name = shieldname
        self.type = shieldtype
        self.basedefn = shieldbasedefn
        self.defn = self.basedefn
        self.maxdur = shielddur
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

    def printshieldinfo(self):
        print('Shield Data: ')
        print('\tLevel:\t\t' + str(self.level))
        print('\tType:\t' + str(self.type))
        print('\tBase defense:\t\t' + str(self.basedefn))
        print('\tDefense:\t\t' + str(self.defn))
        print('\tMax Dur:\t\t\t' + str(self.maxdur))
        print('\tDur:\t\t\t' + str(self.dur))
        print('\tBroken?:\t\t' + str(self.isbroken()))
        print('\tPower:\t' + str(self.power))
