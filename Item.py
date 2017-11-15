class Item:
    # grade,name,effect,value
    def __init__(self, itemlevel, itemgrade, itemname, itemeffect, itemvalue):
        self.level = itemlevel
        self.grade = itemgrade
        self.name = itemname
        self.effect = itemeffect
        self.val = itemvalue

    def printiteminfo(self):
        print('Item: ')
        print('\tLevel:\t\t' + str(self.level))
        print('\tGrade:\t\t' + str(self.grade))
        print('\tName:\t' + str(self.name))
        print('\tEffect Val:\t\t' + str(self.effect))
        print('\tGold Val:\t\t' + str(self.val))
