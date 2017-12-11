import Game


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

    # Heals user up to max health
    def heal(self, hpup):
        Game.centerprint('Enemy heals for ' + str(int(hpup)) + ' HP')
        print('')
        self.hp += hpup
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    # take damage
    def damage(self, hpdown, curve):
        effatk = hpdown + (hpdown * curve)
        self.hp -= int(effatk)
        Game.centerprint(str(self.name) + ' takes ' + str(int(effatk)) + ' damage!')
        if self.hp < 0:
            self.hp = 0

    # resets enemy to max HP (done after a fight)
    def reset(self):
        self.hp = self.maxhp

    # check if enemy is alive
    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

    # enemy running away awards normal XP/Gold to hero for now
    def run(self):
        self.hp = 0

    # enemy could get stronger
    def anger(self):
        Game.centerprint(str(self.name) + ' got Angrier!')
        self.atk += self.atk * .14

    # enemy could get weaker
    def weaker(self):
        Game.centerprint(str(self.name) + ' got Weaker!')
        self.atk -= self.atk * .14

    # prints out all enemy detail
    def printenemyinfodetail(self):
        print(str(self.name))
        print('\tLevel:\t' + str(self.level))
        print('\tAttack:\t' + str(self.atk))
        print('\tXP:\t\t' + str(self.xp))
        print('\tGold:\t' + str(self.gold))
        print('\tMaxHP:\t' + str(self.maxhp))
        print('\tHP:\t\t' + str(self.hp))

    def datadict(self):
        return {'Level': str(self.level),
                'Attack': str(self.atk),
                'XP': str(self.xp),
                'Gold': str(self.gold),
                'MaxHP': str(self.maxhp),
                'HP': str(self.hp)
                }
