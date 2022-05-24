from typing import Optional

import Game


class Enemy:
    def __init__(self,
                 enemy_level: int,
                 enemy_name_1: str,
                 enemy_name_2: str,
                 enemy_name_3: str,
                 enemy_atk: int,
                 enemy_xp: int,
                 enemy_gold: int,
                 enemy_hp: int,
                 enemy_defn: int,
                 enemy_status_effect: Optional[str]):
        self.level = enemy_level
        if enemy_name_2 == enemy_name_3:
            enemy_name_3 = ''
        self.name: str = f'{enemy_name_1} {enemy_name_2} {enemy_name_3}'
        self.atk: int = enemy_atk
        self.xp: int = enemy_xp
        self.gold: int = enemy_gold
        self.max_hp: int = enemy_hp
        self.hp: int = self.max_hp
        self.defn: int = enemy_defn
        self.effect: Optional[str] = enemy_status_effect  # UNUSED

    # Heals user up to max health
    def heal(self, hp_up: int) -> None:
        Game.centerprint(f'Enemy heals for {hp_up} HP\n')
        self.hp += hp_up
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    # take damage
    def damage(self, hp_down: int, curve: int) -> None:
        eff_atk = hp_down + (hp_down * curve)
        self.hp -= int(eff_atk)
        Game.centerprint(f'{self.name} takes {eff_atk} damage!')
        if self.hp < 0:
            self.hp = 0

    # resets enemy to max HP (done after a fight)
    def reset(self) -> None:
        self.hp = self.max_hp

    # check if enemy is alive
    def is_alive(self) -> bool:
        return self.hp > 0

    # enemy running away awards normal XP/Gold to hero for now
    def run(self) -> None:
        self.hp = 0

    # enemy could get stronger
    def anger(self) -> None:
        Game.centerprint(f'{self.name} got angrier!')
        self.atk += self.atk * .14

    # enemy could get weaker
    def weaker(self) -> None:
        Game.centerprint(f'{self.name} got weaker!')
        self.atk -= self.atk * .14

    # prints out all enemy detail
    def print_enemy_info_detail(self) -> None:
        print(str(self.name))
        print('\tLevel:\t' + str(self.level))
        print('\tAttack:\t' + str(self.atk))
        print('\tXP:\t\t' + str(self.xp))
        print('\tGold:\t' + str(self.gold))
        print('\tMaxHP:\t' + str(self.max_hp))
        print('\tHP:\t\t' + str(self.hp))

    def datadict(self) -> dict:
        return {'Level': str(self.level),
                'Attack': str(self.atk),
                'XP': str(self.xp),
                'Gold': str(self.gold),
                'MaxHP': str(self.max_hp),
                'HP': str(self.hp)
                }
