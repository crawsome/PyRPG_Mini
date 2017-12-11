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


# Prints 4 rows of something
def fiverowprintoptions(dataheader, table_data, title):
    marqueeprint(title)
    dataheader.insert(0, '#')
    print("{: <2} {: <10} {: <15} {: <22} {: <6}".format(*dataheader))
    for i, row in enumerate(table_data):
        row.insert(0, i + 1)
        print("{: <2} {: <10} {: <15} {: <22} {: <6}".format(*row))


# dynamic sized row-at-a-time output.
def gridoutput(table_data):
    print(table_data)

    basestring = '{: <'
    cap = '} '
    rowformat = ''

    columwidth = []
    dataheader = table_data.keys()
    dataheader.insert(0, '#')
    print(dataheader)
    # fills array with ints of each columns width
    for i, column in enumerate(table_data):
        print(column)
        columwidth.append(len(max(column.values)))
    print(columwidth)

    for i, headeritem in enumerate(dataheader):
        rowformat += basestring
        rowformat += str(columwidth[i])
        rowformat += cap
    print(rowformat)
    print(rowformat.format(*dataheader))

    rowformat = ''
    for rowitem in table_data:
        rowformat += basestring
        rowformat += str(len(str(rowitem)))
        rowformat += cap
    print(rowformat.format(*dataheader))


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
