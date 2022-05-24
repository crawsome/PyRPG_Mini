import random
from enum import Enum
from typing import Union

from Item import Item
from Shield import Shield
from Weapon import Weapon
from Database import Database
from texttools import *
from Armor import Armor


class HeroClass(Enum):
    HUNTER = 'hunter'
    MAGE = 'mage'
    WARRIOR = 'warrior'


class Hero:
    def __init__(self,
                 hero_class: HeroClass,
                 hero_level: int,
                 hero_hp: int,
                 hero_atk: int,
                 hero_defn: int,
                 hero_next_level: int,
                 hero_dodge: int):
        # name
        self.name: str = ''

        # instance vars
        self.our_class: HeroClass = hero_class
        self.level: int = hero_level
        self.next_level: int = hero_next_level

        # HP
        self.max_hp: int = hero_hp
        self.hp: int = self.max_hp

        # Attack
        self.base_atk: int = hero_atk
        self.atk: int = self.base_atk

        # Defense
        self.base_def: int = hero_defn
        self.defn: int = self.base_def

        # Dodge
        self.base_dodge: int = hero_dodge
        self.dodge: int = self.base_dodge

        # Luck
        self.base_luck: int = 0
        self.luck: int = self.base_luck

        # Crit
        self.base_crit: int = 5
        self.crit: int = self.base_crit

        # game-created vars
        self.gold: int = 0
        self.xp: Union[int, float] = 0

        # Augmentations for hero classes
        self.hp_aug: int = 0
        self.dodge_aug: int = 0
        self.def_aug: int = 0
        self.atk_aug: int = 0
        self.levelup_aug: int = 0
        self.crit_aug: int = 0

        # Items container and usage
        self.items: list = []
        self.active_item = 0

        # Gear container
        self.gear: list = []

        # Keep track of battle count
        self.battle_count: int = 0

        # Used for regen and haste potions
        self.regen_timer: int = 0
        self.haste_timer: int = 0

        # A difficulty curve for determining lots of things
        self.atk_curve: float = 0
        self.def_curve: float = 0

        # equip objects
        self.our_weapon: Weapon = Weapon(0, 'training', 'wooden', 'stick', 3, 20, 'none')
        self.our_armor: Armor = Armor(0, 'training', 'broken', 'plate', 2, 10)
        self.our_shield: Shield = Shield(0, 'training', 'wooden', 'ward', 3, 20)
        self.our_item: Item = Item(0, 0, 0, 0, 0)
        self.is_battling: bool = False

        # width of centered data in screen center
        self.data_width: int = 40

    # Heals user up to max health
    def heal(self, hp_up: int) -> None:
        centerprint(f'You heal for {hp_up} HP\n')
        self.hp += hp_up
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    # flip a coin, pay 100g, 1/2 chance of regaining health
    def heal_flip(self) -> None:
        marqueeprint('[HEAL FLIP]')
        centerprint('Death appears to flip a coin with you.')
        if self.gold >= 100:
            self.gold -= 100
            if random.choice([True, False]):
                self.heal(self.max_hp)
                marqueeprint('[HEAL SUCCESS]')
                centerprint(str(self.max_hp) + ' healed')
                return
            marqueeprint('HEAL FAILED You lost the roll!')
            return
        marqueeprint('[HEAL FAILED]')
        centerprint('You don\'t have enough money!')

    # sometimes you find food after a fight
    def food(self) -> None:
        hp_back = int(self.max_hp * .2)
        centerprint(f'You found some food and healed {hp_back} HP.')
        self.heal(hp_back)

    # take damage
    def damage(self, hp_down: int) -> None:
        eff_atk = hp_down + (hp_down * self.def_curve)
        self.hp -= int(eff_atk)
        centerprint(f'{self.name} takes {eff_atk} damage!')
        self.hp = 0 if self.hp < 0 else self.hp

    # kills the character
    def death(self) -> None:
        self.is_battling = False
        self.hp = 0
        marqueeprint('')
        marqueeprint('[GAME OVER]')
        marqueeprint('\n')
        gridoutput(self.datadict())

    # adds XP to character, and levels up if it goes over
    def add_xp(self, gained_xp: float) -> None:
        gained_xp = gained_xp + (gained_xp * self.def_curve)
        centerprint(f'You gained {gained_xp} Exp')
        self.xp += gained_xp
        if self.xp >= self.next_level:
            self.level_up()

    # adds gold to character
    def add_gold(self, gained_gold: int) -> None:
        gained_gold = gained_gold + (gained_gold * self.def_curve)
        centerprint(f'You gained {str(int(gained_gold + (gained_gold * self.def_curve)))} Gold')
        self.gold += int(gained_gold + (gained_gold * self.def_curve))

    # attempt to buy an item
    def buy_item(self, item: Item) -> None:
        if self.can_afford(item.val):
            self.gold -= item.val
            self.items.append(item)
            print('You bought ' + item.name)
        else:
            print('You can\'t afford that!')

    # see if you can afford an item
    def can_afford(self, val: int) -> bool:
        return self.gold >= val

    # alive check
    def is_alive(self) -> bool:
        return self.hp > 0

    # applies hero's perks
    def hero_perks(self) -> None:
        if self.our_class == HeroClass.WARRIOR:
            # more HP
            self.hp_aug = 15
            # slower
            self.dodge_aug = 2
            # more def
            self.def_aug = 12
            # low atk
            self.atk_aug = 2
            # doofus is a slow leveler
            self.levelup_aug = 1
            # mild crit chance boost
            self.crit_aug = 2
        elif self.our_class == HeroClass.MAGE:
            # glass cannon
            self.hp_aug = 5
            # med dodge
            self.dodge_aug = 5
            # low DEF
            self.def_aug = 6
            # lower atk
            self.atk_aug = 12
            # smarter, levels up quicker
            self.levelup_aug = .6
            # mild crit chance boost
            self.crit_aug = 2
        elif self.our_class == HeroClass.HUNTER:
            # med health
            self.hp_aug = 10
            # high dodge
            self.dodge_aug = 8
            # med DEF
            self.def_aug = 8
            # def ATK
            self.atk_aug = 6
            # he gets by
            self.levelup_aug = .8
            # high crit chance boost
            self.crit_aug = 6
        self.max_hp += self.hp_aug
        self.hp += self.hp_aug
        self.dodge += self.dodge_aug
        self.base_def += self.def_aug
        self.defn += self.def_aug
        self.next_level = int(self.next_level * self.levelup_aug)
        self.base_atk += self.atk_aug
        self.atk += self.atk_aug

    # prints all hero stat info
    def print_hero_info_detail(self) -> None:
        marqueeprint('[HERO DATA]')
        centerprint(lr_justify('Class:', str(self.our_class), self.data_width))
        centerprint(lr_justify('Name:', str(self.name), self.data_width))
        centerprint(lr_justify('Level:', str(self.level), self.data_width))
        centerprint(lr_justify('XP:', str(self.xp) + '/' + str(self.next_level), self.data_width))
        centerprint(lr_justify('HP:', str(self.hp) + '/' + str(self.max_hp), self.data_width))
        centerprint(lr_justify('Gold:', str(self.gold), self.data_width))
        centerprint(lr_justify('Atk:', str(self.atk), self.data_width))
        centerprint(lr_justify('Defense:', str(self.defn), self.data_width))
        centerprint(lr_justify('Dodge:', str(self.dodge), self.data_width))
        centerprint(lr_justify('battles fought', str(self.battle_count), self.data_width))
        print('')

    # returns a dictionary of relevant user data for printing and delivering class information in a package
    def datadict(self) -> dict:
        return {
            'Class': str(self.our_class),
            'Name': str(self.name),
            'Level': str(self.level),
            'XP': str(str(self.xp) + '/' + str(self.next_level)),
            'HP': str(str(self.hp) + '/' + str(self.max_hp)),
            'Gold': str(self.gold),
            'Atk': str(self.atk),
            'Def': str(self.defn),
            'Dodge': str(self.dodge),
            'battles': str(self.battle_count)
        }

    # levels up hero
    def level_up(self) -> None:
        new_db = Database()
        marqueeprint('[LEVEL UP]')
        self.xp -= self.next_level
        self.level += 1
        if self.level > 15:
            centerprint('MAX LEVEL! YOU WIN!')
            centerprint('THANKS FOR PLAYING')
            gridoutput(self.datadict())
            quit()
        new_db.conn.execute('SELECT * FROM levelnotes WHERE level = ' + str(self.level) + ';')
        rows = new_db.conn.fetchall()
        new_db.conn.close()
        new_hero_data = rows[0]
        self.max_hp = int(new_hero_data[1] + self.hp_aug)
        self.hp = self.max_hp
        self.base_atk = int(new_hero_data[2] + self.atk_aug)
        self.atk = self.base_atk
        self.base_def = int(new_hero_data[3] + self.def_aug)
        self.defn = self.base_def
        self.next_level += int(new_hero_data[4] * self.levelup_aug)
        self.dodge = int(new_hero_data[5] + self.dodge_aug)
        self.base_crit += self.crit_aug
        gridoutput(self.datadict())

    # fetches a new weapon for hero
    def new_weapon(self) -> Weapon:
        new_db = Database()
        new_db.conn.execute('SELECT * FROM weapons WHERE "level" = ? AND "class" = ? ;',
                            (str(self.level), str(self.our_class),))
        rows = new_db.conn.fetchall()
        new_db.conn.close()
        new_weapon_data = rows[0]
        our_new_weapon = Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3],
                                new_weapon_data[4], new_weapon_data[5], new_weapon_data[6])
        return our_new_weapon

    # fetches a new armor for hero
    def new_armor(self) -> Armor:
        new_db = Database()
        new_db.conn.execute('SELECT * FROM armor WHERE "level" = ? AND "class" = ? ;',
                            (str(self.level), str(self.our_class),))
        rows = new_db.conn.fetchall()
        new_db.conn.close()
        new_armor_data = rows[0]
        our_new_armor = Armor(new_armor_data[0], new_armor_data[1], new_armor_data[2], new_armor_data[3],
                              new_armor_data[4], new_armor_data[5])
        return our_new_armor

    # fetches a new shield for hero
    def new_shield(self) -> Shield:
        new_db = Database()
        new_db.conn.execute('SELECT * FROM shields WHERE "level" = ? AND "class" = ? ;',
                            (str(self.level), str(self.our_class),))
        rows = new_db.conn.fetchall()
        new_db.conn.close()
        new_shield_data = rows[0]
        our_new_shield = Shield(new_shield_data[0], new_shield_data[1], new_shield_data[2], new_shield_data[3],
                                new_shield_data[4], new_shield_data[5])
        return our_new_shield

    # fetches a new item for hero
    def new_item(self) -> Item:
        new_db = Database()
        new_db.conn.execute('SELECT * FROM items WHERE "level" = ? ;', (self.level,))
        rows = new_db.conn.fetchall()
        new_db.conn.close()
        new_item_data = random.choice(rows)
        our_new_item = Item(new_item_data[0], new_item_data[1], new_item_data[2], new_item_data[3], new_item_data[4])
        return our_new_item

    # re-equips all gear. Usually called when setting something like self.our_armor = Armor.Armor(*args)
    def apply_equip(self) -> None:
        self.atk = int(self.base_atk + self.our_weapon.baseatk)
        self.defn = int(self.base_def + self.our_armor.defn + self.our_shield.defn)
