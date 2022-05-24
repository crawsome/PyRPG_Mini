from enum import Enum

from texttools import *


class ItemGrade(Enum):
    WEAK = 'weak'
    MINOR = 'minor'
    STANDARD = 'standard'
    SATISFYING = 'satisfying'
    EXCESSIVE = 'excessive'
    ABOVE_AVERAGE = 'above average'
    PURE = '100% pure'


class Item:
    # grade,name,effect,value
    def __init__(self,
                 item_level: int,
                 item_grade: ItemGrade,
                 item_name: str,
                 item_effect: int,
                 item_value: int):
        self.level: int = item_level
        self.grade: ItemGrade = item_grade
        self.name: str = item_name
        self.effect: int = item_effect
        self.val: int = item_value

    # prints all item stats
    def print_item_info(self) -> None:
        marqueeprint('Item: ')
        print(lr_justify('Level:', str(self.level), 60))
        print(lr_justify('Grade:', str(self.grade), 60))
        print(lr_justify('Name:', self.name, 60))
        print(lr_justify('Effect Val:', str(self.effect), 60))
        print(lr_justify('Gold Val:', str(self.val), 60))

    # ['Level', 'Quality', 'Name', 'Effect']
    def datadict(self) -> dict:
        return {'Level': str(self.level),
                'Name': str(self.grade) + ' ' + str(self.name),
                'Effect': str(self.effect),
                'Value': str(self.val)
                }
