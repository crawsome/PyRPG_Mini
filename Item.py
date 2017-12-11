from texttools import *


class Item:
    # grade,name,effect,value
    def __init__(self, itemlevel, itemgrade, itemname, itemeffect, itemvalue):
        self.level = itemlevel
        self.grade = itemgrade
        self.name = itemname
        self.effect = itemeffect
        self.val = itemvalue

    # prints all item stats
    def printiteminfo(self):
        marqueeprint('Item: ')
        print(lr_justify('Level:', str(self.level), 60))
        print(lr_justify('Grade:', str(self.grade), 60))
        print(lr_justify('Name:', str(self.name), 60))
        print(lr_justify('Effect Val:', str(self.effect), 60))
        print(lr_justify('Gold Val:', str(self.val), 60))

    # ['Level', 'Quality', 'Name', 'Effect']
    def datadict(self):
        return {'Level': str(self.level),
                'Name': str(self.grade) + ' ' + str(self.name),
                'Effect': str(self.effect),
                'Value': str(self.val)
                }
