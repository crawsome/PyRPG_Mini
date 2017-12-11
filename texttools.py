import textwrap
from difflib import SequenceMatcher


def marqueeprint(text):
    print('{:=^60}'.format(text))


# Left-justify print
def leftprint(text):
    print('{:<60}'.format(text))


# right-justify print
def rightprint(text):
    print('{:>60}'.format(text))


# centered print
def centerprint(text):
    wrapstring = textwrap.wrap(text, width=60)
    for line in wrapstring:
        # print(line)
        print('{:^60}'.format(line))


# From https://stackoverflow.com/questions/9660109/allign-left-and-right-in-python
def lr_justify(left, right, width):
    return '{}{}{}'.format(left, ' ' * (width - len(left + right)), right)


# Prints 4 rows of something with numeric options on left
def fiverowprintoptions(dataheader, table_data, title):
    marqueeprint(title)
    dataheader.insert(0, '#')
    print("{: <2} {: <10} {: <15} {: <22} {: <6}".format(*dataheader))
    for i, row in enumerate(table_data):
        row.insert(0, i + 1)
        print("{: <2} {: <10} {: <15} {: <22} {: <6}".format(*row))


# dynamic sized row-at-a-time output. Will appropriately size the margins
# of any dict passed to it and print it out all pretty-like.
def gridoutput(table_data):
    basestring = '{: <'
    cap = '} '
    rowformat = ''
    columwidth, thedata, dataheader = [], [], []
    for key, value in table_data.items():
        dataheader.append(key)
        thedata.append(value)
        columwidth.append(len(max(key, value)) + 3)
    for i, headeritem in enumerate(dataheader):
        rowformat += basestring
        rowformat += str(columwidth[i])
        rowformat += cap
    marqueeprint(('[' + table_data['Name'] + ']').upper())
    print(rowformat.format(*dataheader))
    print(rowformat.format(*thedata))



# for debugging and margin adjustments for user to zoom in
def printtest():
    marqueeprint("[[PRINT TEST]]")
    leftprint('Justified Left')
    rightprint('Justified Right')
    centerprint('Center Print')


# if string is at least 60% similar, will return true
def similarstring(a, b):
    ourratio = SequenceMatcher(None, a, b).ratio()
    if ourratio >= .8:
        return True
    else:
        return False
