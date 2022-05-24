import random
from enum import Enum
from texttools import *


class ArmorType(Enum):
    OUTFIT = 'outfit'
    PLATE = 'plate'
    ROBE = 'robe'


class ArmorQuality(Enum):
    RUSTY = 'rusty'
    COMMON = 'common'
    GREAT = 'great'
    MAGICAL = 'magical'
    LEGENDARY = 'legendary'


class Armor:
    def __init__(self,
                 armor_level: int,
                 armor_class_type: str,
                 armor_name: str,
                 armor_type: ArmorType,
                 armor_base_def: int,
                 armor_dur: int):
        # level
        self.level: int = armor_level

        # hero Class
        self.class_type: str = armor_class_type

        # hero Class
        self.type: ArmorType = armor_type
        self.name: str = armor_name

        # Armor Quality (rusty, common, great, magical, legendary)
        chance: int = random.randint(1, 100)

        if chance < 20:
            self.quality = ArmorQuality.RUSTY
        elif chance >= 21 or chance < 65:
            self.quality = ArmorQuality.COMMON
        elif chance >= 66 or chance < 86:
            self.quality = ArmorQuality.GREAT
        elif chance >= 85 or chance < 96:
            self.quality = ArmorQuality.MAGICAL
        elif chance >= 96 or chance < 100:
            self.quality = ArmorQuality.LEGENDARY

        # Defense Values
        self.base_defn = armor_base_def
        if self.quality == 'Rusty':
            self.base_defn = int(self.base_defn * 0.9)
        elif self.quality == 'Common':
            self.base_defn = int(self.base_defn * 1)
        elif self.quality == 'Great':
            self.base_defn = int(self.base_defn * 1.25)
        elif self.quality == 'Magical':
            self.base_defn = int(self.base_defn * 1.6)
        elif self.quality == 'Legendary':
            self.base_defn = int(self.base_defn * 2)

        self.defn = self.base_defn

        # armor durability value
        self.max_dur = armor_dur
        if self.quality == 'Rusty':
            self.max_dur = int(self.max_dur * 0.9)
        elif self.quality == 'Common':
            self.max_dur = int(self.max_dur * 1)
        elif self.quality == 'Great':
            self.max_dur = int(self.max_dur * 1.25)
        elif self.quality == 'Magical':
            self.max_dur = int(self.max_dur * 1.6)
        elif self.quality == 'Legendary':
            self.max_dur = int(self.max_dur * 2)
        self.dur = self.max_dur

    # damage durability, and check to see if broken
    def damage_dur(self, aug, curve) -> None:
        self.dur -= int(aug * curve * .1)
        self.is_broken()

    # restore dur and check to see if fixed
    def restore_dur(self, aug) -> None:
        self.dur += aug
        if self.dur > self.max_dur:
            self.dur = self.max_dur
        if not self.is_broken():
            self.defn = self.base_defn

    # repair entirely
    def repair(self) -> None:
        self.defn = self.base_defn
        self.dur = self.max_dur

    # 15% durability = stat reduction
    def is_broken(self) -> bool:
        if self.dur <= 0:
            self.gear_break()
            return True
        return False

    # this breaks the gear
    def gear_break(self) -> None:
        # Possible FixMe: self.atk seems to serve no purpose
        self.atk = int(self.base_defn * .3)

    # prints all armor info
    def print_armor_info(self) -> None:
        marqueeprint('ARMOR')
        print(lr_justify('Level:', str(self.level), 60))
        print(lr_justify('Name:', str(self.name), 60))
        print(lr_justify('Type:', str(self.type), 60))
        print(lr_justify('Defense:', str(self.defn) + '/' + str(self.base_defn), 60))
        print(lr_justify('Dur:', str(self.dur) + '/' + str(self.max_dur), 60))
        print(lr_justify('Broken?:', 'Yes' if self.is_broken() else 'No', 60))
        print(lr_justify('Quality:', str(self.quality), 60))

    # {'Level', 'Name', 'Type', 'Defense', 'Dur', 'Broken?', 'Power'}
    def datadict(self) -> dict:
        return {'Level': str(self.level),
                'Name': f'{self.name} {self.type}',
                'Def': str(self.defn),
                'Dur': f'{self.dur} / {self.max_dur}',
                'Broken?': str(self.is_broken()),
                'Repair Cost': f'{str(self.max_dur - self.dur)} gold',
                'Quality': str(self.quality)
                }
