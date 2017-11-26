import csv
import os
from sqlite3 import connect

import Game


class dbsetup():
    def __init__(self):
        self.dbpath = './db/game.db'
        # import and create our player database
        self.gamedb = connect(self.dbpath)
        self.conn = self.gamedb.cursor()

    # used to delete the current database
    def deletedbifexists(self):
        if os.path.exists('./db/game.db'):
            os.remove('./db/game.db')

    def setupdb(self):
        # If you set this to 1, it will print out all data as it populates the datbase.
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
            '''CREATE TABLE IF NOT EXISTS armor (level INTEGER, class TEXT, name TEXT, type TEXT, basedef INTEGER, durability INTEGER)''')

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
            '''CREATE TABLE IF NOT EXISTS items(level INT, grade INT,name TEXT,effect INT,value INT)''')

        # insert our items table in the database
        if debugging:
            print('inserting items into database')
        with open('./csv/items.csv', 'r') as fin:
            dr = csv.reader(fin)
            for i in dr:
                if debugging:
                    print('inserting ' + str(i))
                cur.execute('INSERT INTO items VALUES (?,?,?,?,?);', i)
            if debugging:
                cur.execute('SELECT * FROM items')
                rows = cur.fetchall()
                for row in rows:
                    print('QUERY ALL: ' + str(row))

        # create our levelnotes table in the database
        if debugging:
            print('creating table for levelnotes')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS levelnotes(Level INT,HP INT,ATK INT,DEF INT,xptonextlevel INT, dodge INT )''')

        # insert our levelnotes table in the database
        if debugging:
            print('inserting levelnotes into database')
        with open('./csv/levelnotes.csv', 'r') as fin:
            dr = csv.reader(fin)
            for i in dr:
                if debugging:
                    print('inserting ' + str(i))
                cur.execute('INSERT INTO levelnotes VALUES (?,?,?,?,?,?);', i)
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
            '''CREATE TABLE IF NOT EXISTS weapons ( level INTEGER ,class TEXT ,name TEXT ,type TEXT,baseattack INTEGER ,durability INTEGER ,power TEXT)''')

        # insert our weapons table in the database
        if debugging:
            print('inserting weapons into database')
        with open('./csv/weapons.csv', 'r') as fin:
            dr = csv.reader(fin)
            for i in dr:
                if debugging:
                    print('inserting ' + str(i))
                cur.execute('INSERT INTO weapons VALUES (?,?,?,?,?,?,?);', i)
            if debugging:
                cur.execute('SELECT * FROM weapons')
                rows = cur.fetchall()
                for row in rows:
                    print('QUERY ALL: ' + str(row))

        # create our riddles table in the database
        if debugging:
            print('creating table for riddles')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS riddles (question TEXT ,answer TEXT)''')

        # insert our riddles table in the database
        if debugging:
            print('inserting riddles into database')
        with open('./csv/riddles.csv', 'r') as fin:
            dr = csv.reader(fin)
            for i in dr:
                if debugging:
                    print('inserting ' + str(i))
                cur.execute('INSERT INTO riddles VALUES (?,?);', i)
            if debugging:
                cur.execute('SELECT * FROM riddles')
                rows = cur.fetchall()
                for row in rows:
                    print('QUERY ALL: ' + str(row))
        # commit the changes
        conn.commit()
        # close the database connection to let other operations use it
        conn.close()
        Game.centerprint('...Have fun')
