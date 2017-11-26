import Game


# TODO: Make shield, armor, weapon all have similar repair methods.
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

    # damage durability, and check to see if broken
    def damagedur(self, aug, curve):
        self.dur -= int(aug * curve)
        self.isbroken()
        pass

    # restore dur and check to see if fixed
    def restoredur(self, aug):
        self.dur += aug
        if self.dur > self.maxdur:
            self.dur = self.maxdur
        if not self.isbroken():
            self.defn = self.basedefn

    # repair entirely
    def repair(self):
        self.defn = self.basedefn
        self.dur = self.maxdur

    # 15% durability = stat reduction
    def isbroken(self):
        if self.dur <= 0:
            self.gearbreak()
            return True
        elif self.dur > 0:
            return False

    # this breaks the gear
    def gearbreak(self):
        self.atk = int(self.basedefn * .3)

    def printshieldinfo(self):
        Game.marqueeprint('SHIELD')
        print(Game.lr_justify('Level:', str(self.level), 50))
        print(Game.lr_justify('Name:', str(self.name), 50))
        print(Game.lr_justify('Type:', str(self.type), 50))
        print(Game.lr_justify('Defense:', str(self.defn) + '/' + str(self.basedefn), 50))
        print(Game.lr_justify('Dur:', str(self.dur) + '/' + str(self.maxdur), 50))
        print(Game.lr_justify('Broken?:', str(self.isbroken()), 50))
