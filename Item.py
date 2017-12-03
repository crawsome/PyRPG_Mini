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
        print(Game.lr_justify('Level:', str(self.level), 60))
        print(Game.lr_justify('Grade:', str(self.grade), 60))
        print(Game.lr_justify('Name:', str(self.name), 60))
        print(Game.lr_justify('Effect Val:', str(self.effect), 60))
        print(Game.lr_justify('Gold Val:', str(self.val), 60))

    def getitemdata(self):
        return [str(self.level), str(self.grade), str(self.name), str(self.effect)]
