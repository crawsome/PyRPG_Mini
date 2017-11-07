class Item:

    # grade,name,effect,value
    def __init__(self, itemgrade, itemname, itemeffect, itemvalue):
        self.grade = itemgrade
        self.name = itemname
        self.effect = itemeffect
        self.val = itemvalue

    def printiteminfo(self):
        print('Item Data: ')
        print('\tGrade:\t\t' + str(self.grade))
        print('\tName:\t' + str(self.name))
        print('\tEffect Val:\t\t' + str(self.effect))
        print('\tGold Val:\t\t' + str(self.val))
