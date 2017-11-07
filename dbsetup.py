import csv
from sqlite3 import connect


def setup():
    debugging = 0

    # make a database connection to the game database
    if debugging:
        print('connecting to database')
    conn = connect('./db/game.db')

    # create our cursor
    if debugging:
        print('creating cursor')
    cur = conn.cursor()

    # create our armor table in the database
    if debugging:
        print('creating table for armor')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS armor (level INTEGER, classtype TEXT, name TEXT, type TEXT, basedef INTEGER, durability INTEGER)''')

    # insert our armor table in the database
    if debugging:
        print('inserting armor into database')
    with open('./csv/armor.csv', 'r') as fin:
        dr = csv.reader(fin)
        for i in dr:
            if debugging:
                print('inserting ' + str(i))
            cur.execute('INSERT INTO armor VALUES (?,?,?,?,?,?);', i)
        if debugging:
            cur.execute('SELECT * FROM armor')
            rows = cur.fetchall()
            for row in rows:
                print('QUERY ALL: ' + str(row))

    # create our enemy table in the database
    if debugging:
        print('creating table for enemies')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS enemies(level INT, firstname TEXT, middlename TEXT, lastname TEXT, attack INTEGER, xp INTEGER, gold INTEGER, hp INTEGER, def INTEGER, status TEXT)''')

    # insert our enemy table in the database
    if debugging:
        print('inserting enemies into database')
    with open('./csv/enemies.csv', 'r') as fin:
        dr = csv.reader(fin)
        for i in dr:
            if debugging:
                print('inserting ' + str(i))
            cur.execute('INSERT INTO enemies VALUES (?,?,?,?,?,?,?,?,?,?);', i)
        if debugging:
            cur.execute('SELECT * FROM enemies')
            rows = cur.fetchall()
            for row in rows:
                print('QUERY ALL: ' + str(row))

    # create our items table in the database
    if debugging:
        print('creating table for items')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS items(grade INT,name TEXT,effect INT,value INT)''')

    # insert our items table in the database
    if debugging:
        print('inserting items into database')
    with open('./csv/items.csv', 'r') as fin:
        dr = csv.reader(fin)
        for i in dr:
            if debugging:
                print('inserting ' + str(i))
            cur.execute('INSERT INTO items VALUES (?,?,?,?);', i)
        if debugging:
            cur.execute('SELECT * FROM items')
            rows = cur.fetchall()
            for row in rows:
                print('QUERY ALL: ' + str(row))

    # create our levelnotes table in the database
    if debugging:
        print('creating table for levelnotes')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS levelnotes(Level INT,HP INT,ATK INT,DEF INT,xptonextlevel INT )''')

    # insert our levelnotes table in the database
    if debugging:
        print('inserting levelnotes into database')
    with open('./csv/levelnotes.csv', 'r') as fin:
        dr = csv.reader(fin)
        for i in dr:
            if debugging:
                print('inserting ' + str(i))
            cur.execute('INSERT INTO levelnotes VALUES (?,?,?,?,?);', i)
        if debugging:
            cur.execute('SELECT * FROM levelnotes')
            rows = cur.fetchall()
            for row in rows:
                print('QUERY ALL: ' + str(row))

    # create our shields table in the database
    if debugging:
        print('creating table for shields')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS shields (level INT,class TEXT,name TEXT,type TEXT,basedef INT,durability INT)''')

    # insert our shields table in the database
    if debugging:
        print('inserting shields into database')
    with open('./csv/shields.csv', 'r') as fin:
        dr = csv.reader(fin)
        for i in dr:
            if debugging:
                print('inserting ' + str(i))
            cur.execute('INSERT INTO shields VALUES (?,?,?,?,?,?);', i)
        if debugging:
            cur.execute('SELECT * FROM shields')
            rows = cur.fetchall()
            for row in rows:
                print('QUERY ALL: ' + str(row))

    # create our weapons table in the database
    if debugging:
        print('creating table for weapons')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS weapons ( level INTEGER ,name TEXT ,type TEXT,baseattack INTEGER ,durability INTEGER ,power TEXT)''')

    # insert our weapons table in the database
    if debugging:
        print('inserting weapons into database')
    with open('./csv/weapons.csv', 'r') as fin:
        dr = csv.reader(fin)
        for i in dr:
            if debugging:
                print('inserting ' + str(i))
            cur.execute('INSERT INTO weapons VALUES (?,?,?,?,?,?);', i)
        if debugging:
            cur.execute('SELECT * FROM weapons')
            rows = cur.fetchall()
            for row in rows:
                print('QUERY ALL: ' + str(row))
    conn.commit()
