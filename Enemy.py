from Game import centerprint


class Enemy:
    def __init__(self, enemylevel, enemyname1, enemyname2, enemyname3, enemyatk, enemyxp, enemygold, enemyhp, enemydefn,
                 enemystatuseffect):
        self.level = enemylevel
        if enemyname2 == enemyname3:
            enemyname3 = ''
        self.name = str(enemyname1) + ' ' + str(enemyname2) + ' ' + str(enemyname3)
        self.atk = enemyatk
        self.xp = enemyxp
        self.gold = enemygold
        self.maxhp = enemyhp
        self.hp = self.maxhp
        self.defn = enemydefn
        self.effect = enemystatuseffect

    def heal(self, hpup):
        self.hp += hpup
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def damage(self, hpdown):
        self.hp -= hpdown
        if self.hp < 0:
            self.hp = 0

    def reset(self):
        self.hp = self.maxhp

    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

    def run(self):
        self.hp = 0

    def anger(self):
        centerprint(str(self.name) + ' got Angrier!')
        self.atk += self.atk * .14

    def weaker(self):
        centerprint(str(self.name) + ' got Weaker!')
        self.atk -= self.atk * .14

    def printenemyinfodetail(self):
        print(str(self.name))
        print('\tLevel:\t' + str(self.level))
        print('\tAttack:\t' + str(self.atk))
        print('\tXP:\t\t' + str(self.xp))
        print('\tGold:\t' + str(self.gold))
        print('\tMaxHP:\t' + str(self.maxhp))
        print('\tHP:\t\t' + str(self.hp))
