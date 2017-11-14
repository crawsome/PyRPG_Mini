class Hero:
    def __init__(self, heroclass, herolevel, herohp, heroatk, herodefn, heronextlevel, herododge):
        self.name = ''
        self.ourclass = heroclass
        self.level = herolevel
        self.maxhp = herohp
        self.hp = self.maxhp
        self.baseatk = heroatk
        self.atk = self.baseatk
        self.basedef = herodefn
        self.defn = self.basedef
        self.nextlevel = heronextlevel
        self.gold = 0
        self.dodge = herododge
        self.items = [0, 0, 0, 0]
        self.xp = 0
        self.isbattling = False
        self.hpaug = 0
        self.dodgeaug = 0
        self.defaug = 0
        self.levelupaug = 0

    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

    def heroperks(self):
        if self.ourclass == 'Warrior':
            self.hpaug = 15
            self.dodgeaug = 2
            self.defaug = 12
            self.atkaug = 2
            self.levelupaug = 1
        elif self.ourclass == 'Mage':
            self.hpaug = 5
            self.dodgeaug = 5
            self.defaug = 6
            self.atkaug = 12
            self.levelupaug = .7
        elif self.ourclass == 'Hunter':
            self.hpaug = 10
            self.dodgeaug = 8
            self.defaug = 8
            self.atkaug = 6
            self.levelupaug = .9
        self.maxhp += self.hpaug
        self.hp += self.hpaug
        self.dodge += self.dodgeaug
        self.basedef += self.defaug
        self.defn += self.defaug
        self.nextlevel = int(self.nextlevel * self.levelupaug)
        self.baseatk += self.atkaug
        self.atk += self.atkaug

    def printheroinfo(self):
        print(self.name + '\nHP:\t' + str(self.hp) + '\n')

    def printheroinfodetail(self):
        print('Hero Data: ')
        print('\tClass:\t\t' + str(self.ourclass))
        print('\tName:\t\t' + str(self.name))
        print('\tLevel:\t\t' + str(self.level))
        print('\tMax HP:\t\t' + str(self.maxhp))
        print('\tCurrent HP:\t' + str(self.hp))
        print('\tGold:\t\t' + str(self.gold))
        print('\tAtk:\t\t' + str(self.atk))
        print('\tDefense:\t' + str(self.defn))
        print('\tDodge:\t\t' + str(self.dodge))
        print('\tXP:\t\t\t' + str(self.xp))
        print('\tNextLvl:\t' + str(self.nextlevel))

