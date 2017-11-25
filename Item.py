import Game


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
        Game.marqueeprint('Item: ')
        print(Game.lr_justify('Level:', str(self.level), 50))
        print(Game.lr_justify('Grade:', str(self.grade), 50))
        print(Game.lr_justify('Name:', str(self.name), 50))
        print(Game.lr_justify('Effect Val:', str(self.effect), 50))
        print(Game.lr_justify('Gold Val:', str(self.val), 50))
