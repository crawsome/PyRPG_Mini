import Game
import random


# TODO: Make shield, armor, weapon all have similar repair methods.
class Shield:
    # level,class,name,type,basedef,durability
    def __init__(self, shieldlevel, shieldclass, shieldname, shieldtype, shieldbasedefn, shielddur):
        # shield level
        self.level = shieldlevel

        # shield hero class type
        self.ourshieldclass = shieldclass

        # shield name
        self.name = shieldname

        # shield type
        self.type = shieldtype

        # Shield Quality (rusty, common, great, magical, legendary)
        chance = random.randint(1, 100)

        if chance < 20:
            self.quality = 'Rusty'
        elif chance >= 21 or chance < 65:
            self.quality = 'Common'
        elif chance >= 66 or chance < 86:
            self.quality = 'Great'
        elif chance >= 85 or chance < 96:
            self.quality = 'Magical'
        elif chance >= 96 or chance < 100:
            self.quality = 'Legendary'

        # Defense Values
        self.basedefn = shieldbasedefn
        if self.quality == 'Rusty':
            self.basedefn = int(self.basedefn * 0.9)
        elif self.quality == 'Common':
            self.basedefn = int(self.basedefn * 1)
        elif self.quality == 'Great':
            self.basedefn = int(self.basedefn * 1.25)
        elif self.quality == 'Magical':
            self.basedefn = int(self.basedefn * 1.6)
        elif self.quality == 'Legendary':
            self.basedefn = int(self.basedefn * 2)

        self.defn = self.basedefn

        # shield durability value
        self.maxdur = shielddur
        if self.quality == 'Rusty':
            self.maxdur = int(self.maxdur * 0.9)
        elif self.quality == 'Common':
            self.maxdur = int(self.maxdur * 1)
        elif self.quality == 'Great':
            self.maxdur = int(self.maxdur * 1.25)
        elif self.quality == 'Magical':
            self.maxdur = int(self.maxdur * 1.6)
        elif self.quality == 'Legendary':
            self.maxdur = int(self.maxdur * 2)
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

    # prints all info about the shield
    def printshieldinfo(self):
        Game.marqueeprint('SHIELD')
        print(Game.lr_justify('Level:', str(self.level), 60))
        print(Game.lr_justify('Name:', str(self.name), 60))
        print(Game.lr_justify('Type:', str(self.type), 60))
        print(Game.lr_justify('Defense:', str(self.defn) + '/' + str(self.basedefn), 60))
        print(Game.lr_justify('Dur:', str(self.dur) + '/' + str(self.maxdur), 60))
        print(Game.lr_justify('Broken?:', str(self.isbroken()), 60))
        print(Game.lr_justify('Quality:', str(self.quality), 60))

    # ['Level', 'Name', 'Defense', 'Dur', 'Broken?', 'Power']
    def datadict(self):
        return {'Level': str(self.level),
                'Name': str(self.name) + ' ' + str(self.type),
                'Def': str(self.defn),
                'Dur': str(self.dur) + '/' + str(self.maxdur),
                'Broken?': str(self.isbroken()),
                'Repair Cost': str(self.maxdur - self.dur) + ' gold',
                'Quality': str(self.quality)
                }
