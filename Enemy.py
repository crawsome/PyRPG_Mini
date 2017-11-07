class Enemy:
    def __init__(self, enemylevel, enemyname1, enemyname2, enemyname3, enemyatk, enemyxp, enemygold, enemyhp, enemydefn,
                 enemystatuseffect):
        self.level = enemylevel
        self.name = str(enemyname1) + ' ' + str(enemyname2) + ' ' + str(enemyname3)
        self.atk = enemyatk
        self.xp = enemyxp

        self.gold = enemygold
        self.maxhp = enemyhp
        self.hp = self.maxhp
        self.defn = enemydefn
        self.effect = enemystatuseffect

    def reset(self):
        self.hp = self.maxhp

    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

    def printenemyinfo(self):
        print('\t' + str(self.name) + ' HP:\t\t' + str(self.hp))

    def allprintenemyinfo(self):
        print('\tLevel:\t' + str(self.level))
        print('\tName:\t' + str(self.name))
        print('\tAttack:\t' + str(self.atk))
        print('\tXP:\t\t' + str(self.xp))
        print('\tGold:\t' + str(self.gold))
        print('\tMaxHP:\t' + str(self.maxhp))
        print('\tHP:\t\t' + str(self.hp))
