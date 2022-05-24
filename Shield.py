import random
from texttools import *


class ShieldType:
    WARD = 'ward'
    SHIELD = 'shield'
    BUCKLER = 'buckler'


class ShieldQuality:
    RUSTY = 'rusty'
    COMMON = 'common'
    GREAT = 'great'
    MAGICAL = 'magical'
    LEGENDARY = 'legendary'


# TODO: Make shield, armor, weapon all have similar repair methods.
# TIP (from @DavidRodenkirchen): Make abstract base class for all of these and implement those methods there
class Shield:
    # level,class,name,type,base_def,durability
    def __init__(self,
                 shield_level: int,
                 shield_class: str,
                 shield_name: str,
                 shield_type: ShieldType,
                 shield_base_defn: int,
                 shield_dur: int):
        # shield level
        self.level: int = shield_level

        # shield hero class type
        self.our_shield_class: str = shield_class

        # shield name
        self.name: str = shield_name

        # shield type
        self.type: ShieldType = shield_type

        self.base_defn = shield_base_defn

        # Shield Quality (rusty, common, great, magical, legendary)
        chance = random.randint(1, 100)

        if chance < 20:
            self.quality = ShieldQuality.RUSTY
            self.base_defn = int(self.base_defn * 0.9)
        elif chance >= 21 or chance < 65:
            self.quality = ShieldQuality.COMMON
            self.base_defn = int(self.base_defn * 1)
        elif chance >= 66 or chance < 86:
            self.quality = ShieldQuality.GREAT
            self.base_defn = int(self.base_defn * 1.25)
        elif chance >= 85 or chance < 96:
            self.quality = ShieldQuality.MAGICAL
            self.base_defn = int(self.base_defn * 1.6)
        elif chance >= 96 or chance < 100:
            self.quality = ShieldQuality.LEGENDARY
            self.base_defn = int(self.base_defn * 2)

        self.defn = self.base_defn

        # shield durability value
        self.max_dur = shield_dur
        if self.quality == ShieldQuality.RUSTY:
            self.max_dur = int(self.max_dur * 0.9)
        elif self.quality == ShieldQuality.COMMON:
            self.max_dur = int(self.max_dur * 1)
        elif self.quality == ShieldQuality.GREAT:
            self.max_dur = int(self.max_dur * 1.25)
        elif self.quality == ShieldQuality.MAGICAL:
            self.max_dur = int(self.max_dur * 1.6)
        elif self.quality == ShieldQuality.LEGENDARY:
            self.max_dur = int(self.max_dur * 2)
        self.dur = self.max_dur

    # damage durability, and check to see if broken
    def damage_dur(self, aug: int, curve: float) -> None:
        self.dur -= int(aug * curve)
        self.is_broken()

    # restore dur and check to see if fixed
    def restore_dur(self, aug: int) -> None:
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

    # prints all info about the shield
    def print_shield_info(self) -> None:
        marqueeprint('SHIELD')
        print(lr_justify('Level:', str(self.level), 60))
        print(lr_justify('Name:', self.name, 60))
        print(lr_justify('Type:', str(self.type), 60))
        print(lr_justify('Defense:', f'{self.defn} / {self.base_defn}', 60))
        print(lr_justify('Dur:', f'{self.dur} / {self.max_dur}', 60))
        print(lr_justify('Broken?:', 'Yes' if self.is_broken() else 'No', 60))
        print(lr_justify('Quality:', str(self.quality), 60))

    # ['Level', 'Name', 'Defense', 'Dur', 'Broken?', 'Power']
    def datadict(self) -> dict:
        return {'Level': str(self.level),
                'Name': str(self.name) + ' ' + str(self.type),
                'Def': str(self.defn),
                'Dur': str(self.dur) + '/' + str(self.max_dur),
                'Broken?': str(self.is_broken()),
                'Repair Cost': f'{str(self.max_dur - self.dur)} + gold',
                'Quality': str(self.quality)
                }
