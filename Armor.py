import Game


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

    def isbroken(self):
        if self.dur <= 0:
            self.defn = int(self.basedefn * .3)
            return True
        else:
            return False

    def repair(self):
        self.defn = self.basedefn
        self.dur = self.maxdur

    def printarmorinfo(self):
        Game.marqueeprint('Armor: ')
        print(Game.lr_justify('Level:', str(self.level), 50))
        print(Game.lr_justify('Name:', str(self.name), 50))
        print(Game.lr_justify('Type:', str(self.type), 50))
        print(Game.lr_justify('Base defense:', str(self.basedefn), 50))
        print(Game.lr_justify('Defense:', str(self.defn), 50))
        print(Game.lr_justify('Max Dur:', str(self.maxdur), 50))
        print(Game.lr_justify('Dur:', str(self.dur), 50))
        print(Game.lr_justify('Broken?:', str(self.isbroken()), 50))
