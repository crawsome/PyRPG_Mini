import Game


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

    def isbroken(self):
        if self.dur <= 0:
            self.defn = int(self.basedefn * .3)
            return True
        else:
            return False

    def repair(self):
        self.defn = self.basedefn
        self.dur = self.maxdur

    def printshieldinfo(self):
        Game.marqueeprint('Shield:')
        print(Game.lr_justify('Level:', str(self.level), 50))
        print(Game.lr_justify('Name:', str(self.name), 50))
        print(Game.lr_justify('Type:', str(self.type), 50))
        print(Game.lr_justify('Base defense:', str(self.basedefn), 50))
        print(Game.lr_justify('Defense:', str(self.defn), 50))
        print(Game.lr_justify('Max Dur:', str(self.maxdur), 50))
        print(Game.lr_justify('Dur:', str(self.dur), 50))
        print(Game.lr_justify('Broken?:', str(self.isbroken()), 50))
