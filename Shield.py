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
        print('Shield:')
        print('\tLevel:\t\t\t' + str(self.level))
        print('\tName:\t\t\t' + str(self.name))
        print('\tType:\t\t\t' + str(self.type))
        print('\tBase defense:\t' + str(self.basedefn))
        print('\tDefense:\t\t' + str(self.defn))
        print('\tMax Dur:\t\t' + str(self.maxdur))
        print('\tDur:\t\t\t' + str(self.dur))
        print('\tBroken?:\t\t' + str(self.isbroken()))
