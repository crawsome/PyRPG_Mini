import datetime
import os
import pickle
import random
import time
from sqlite3 import connect
from typing import Optional

from Hero import Hero, HeroClass
import Enemy
from Database import Database
from texttools import *


# game class makes the game work instantiates all other classes at some point.
class Game:
    def __init__(self):
        # adds a little suspense
        # TODO: add suspense option to some printing methods?
        self.suspense_mode: bool = False

        # provides inner workings of game, some live-comments
        # TODO: add more comments and stats as game goes on
        centerprint('Debugging Mode? [1] for yes, [ENTER] for no')
        self.debugging: bool = input() == "1"

        # riddle mode 0 - optional, 1 - mandatory
        centerprint('Riddles Mandatory? [1] for yes, [ENTER] for no')
        self.riddle_mode: bool = input() == "1"

        # provides a way to speed through battle (risky!)
        self.auto_attack: bool = False

        # initialize variables for hero and enemy objects
        self.our_hero: Optional[Hero] = None
        self.our_enemy: Optional[Enemy] = None

        # global text width
        self.text_width: int = 70

        # width of data, so it's not so spaced-out
        self.data_width: int = 55

        # Create all game databases (only needs to run once to make databases)
        first_time: bool = False
        if 'game.db' not in os.listdir('./db/'):
            centerprint('This looks like it\'s your first time playing.')
            centerprint('We must load the database first')
            centerprint('This will only take a moment...')
            first_time = True

        # re-creates the database, in case you change values1
        if first_time:
            print('Loading Database:')
            database = Database()
            database.setup_db()
        if self.debugging:
            printtest()

        # our database path
        self.dbpath = './db/game.db'

        # import and create our player database
        self.game_db = connect(self.dbpath)
        self.conn = self.game_db.cursor()

    # TODO: make self.our_hero.levelup and newhero the same function
    # makes a new hero object for when starting new game.
    def new_hero(self) -> Hero:
        self.conn.execute('SELECT * FROM levelnotes WHERE level = 1;')
        rows = self.conn.fetchall()
        marqueeprint('[CHOOSE CLASS]')
        centerprint('[w]arrior [m]age [h]unter')
        our_class = input()
        if our_class == 'w' or our_class == '':
            our_class = HeroClass.WARRIOR
        elif our_class == 'm':
            our_class = HeroClass.MAGE
        elif our_class == 'h':
            our_class = HeroClass.HUNTER
        else:
            centerprint('Please enter a valid selection')
            return self.new_hero()
        marqueeprint('[CHOOSE DIFFICULTY]')
        centerprint('[1]easy [2]med [3]hard')
        diff = input()

        # the harder the difficulty, the less your attack and defense
        if diff == '1' or diff == '':
            atk_curve = .2
            def_curve = .05
        elif diff == '2':
            atk_curve = .1
            def_curve = .1
        elif diff == '3':
            atk_curve = .05
            def_curve = .2
        else:
            centerprint('Please enter a valid selection')
            diff = 1
            atk_curve = .4
            def_curve = .05
            centerprint(f'Setting Difficulty to {diff}')

        new_hero_data = rows[0]
        our_new_hero = Hero(our_class,
                            new_hero_data[0], new_hero_data[1],
                            new_hero_data[2], new_hero_data[3],
                            new_hero_data[4], new_hero_data[5])
        our_new_hero.def_curve = def_curve
        our_new_hero.atk_curve = atk_curve
        marqueeprint('[ENTER NAME]')
        centerprint(f'Your name, {our_new_hero.our_class} ?\n')
        new_hero_name = input()
        our_new_hero.name = new_hero_name if new_hero_name else 'Sir Lazy'
        return our_new_hero

    # brings game back after death.
    def game_loop(self) -> None:
        while True:
            marqueeprint('')
            centerprint('MiniRPG')
            centerprint('Colin Burke 2017')
            marqueeprint('')
            centerprint('[n]ew game [l]oad')
            decision = input()
            if decision == 'n' or decision == '':
                # Make new global hero and enemy which will change over time
                self.our_hero = self.new_hero()
                self.our_enemy = self.get_enemy()
                self.our_hero.hero_perks()
                gridoutput(self.our_hero.datadict())
            if decision == 'l':
                print('LOADING GAME')
                self.our_hero = self.load_game()
                self.our_enemy = self.get_enemy()
            while self.our_hero.is_alive():
                self.adventure()

    # where the meat of things happen, this decides what happens when you enter [a]dventure
    def adventure(self):
        centerprint('[a]dventure or [c]amp')
        m = input()
        our_rand = random.randint(0, 100)
        if m == 'a' or m == '':
            if our_rand <= 70:
                self.our_hero.is_battling = True
                # Make new enemy
                self.our_enemy = self.get_enemy()
                marqueeprint('[BATTLE]')
                # battle until one is dead
                turn_num = 1
                while self.our_hero.is_alive() and self.our_enemy.is_alive() and self.our_hero.is_battling:
                    marqueeprint(f'[TURN {turn_num}]')
                    self.battle()
                    turn_num += 1
            elif 70 < our_rand <= 90:
                marqueeprint('[FOUND ITEM]')
                itemrand = random.randrange(0, 6)
                if itemrand == 0:
                    self.our_hero.our_armor = self.our_hero.new_armor()
                    gridoutput(self.our_hero.our_armor.datadict())
                elif itemrand == 1:
                    self.our_hero.our_weapon = self.our_hero.new_weapon()
                    gridoutput(self.our_hero.our_weapon.datadict())
                elif itemrand == 2:
                    self.our_hero.our_shield = self.our_hero.new_shield()
                    gridoutput(self.our_hero.our_shield.datadict())
                elif 3 <= itemrand <= 6:
                    self.our_hero.our_item = self.our_hero.new_item()
                    gridoutput(self.our_hero.our_item.datadict())
                    self.our_hero.items.append(self.our_hero.our_item)
                self.our_hero.apply_equip()
            elif 90 < our_rand <= 95:
                marqueeprint('A LONE TRAVELER')
                centerprint('You find a lone traveler,')
                centerprint('He says:')
                print('\n')
                with open('./quoteslist.txt', 'rb') as f:
                    quote_list = f.read().splitlines()
                    quote = random.choice(quote_list).decode('utf-8')
                    for line in textwrap.wrap(quote, width=self.data_width):
                        centerprint(line)
                    print('\n')
                three_choice_random = random.randrange(0, 2)
                if three_choice_random == 0:
                    xp_gain = int(self.our_hero.next_level * .10)
                    self.our_hero.add_xp(int(round(xp_gain, 1)))
                if three_choice_random == 1:
                    gold_gain = int(self.our_hero.gold * .10)
                    self.our_hero.add_gold(gold_gain)
                if three_choice_random == 2:
                    pass
                centerprint('...you venture back to camp')
            elif 90 < our_rand <= 95:
                # a story event?
                centerprint('You find nothing and wander back to camp')
                pass
            elif 95 < our_rand <= 100:
                self.riddle()
        elif m == 'c':
            self.camp()
        if not self.our_hero.is_alive():
            return

    # One round of a battle
    def battle(self):
        self.our_hero.battle_count += 1
        self.print_adversaries(self.data_width)
        marqueeprint('[CHOOSE ACTION]')
        centerprint('[a]tk  [d]ef [r]un [i]tem')
        centerprint('Coinflip to [h]eal (100g)')
        centerprint('Action?')
        next_move = input()
        # conditions to end battle
        if self.our_hero.is_alive():
            turn_not_used = True
            while turn_not_used:
                turn_not_used = self.player_turn(next_move)
                # wait = input()
        if self.our_enemy.is_alive():
            self.enemy_turn()
            # wait = input()
        if not self.our_hero.is_alive():
            self.our_hero.death()
            # wait = input()
            return
        if not self.our_enemy.is_alive():
            self.our_hero.is_battling = False
            self.our_enemy.reset()
            marqueeprint('[VICTORY]')
            self.our_hero.add_gold(self.our_enemy.gold + (self.our_enemy.gold * self.our_hero.def_curve))
            self.our_hero.add_xp(self.our_enemy.xp + (self.our_enemy.xp * self.our_hero.def_curve))
            # 15% chance to get some health back.
            if random.randrange(0, 100) in range(0, 15):
                self.our_hero.food()
            centerprint('Press [Enter] To continue')
            input()  # Wait
        if not self.our_hero.is_battling:
            return

    # One round of a player's turn
    def player_turn(self, m: str) -> Optional[bool]:  # FixMe: This stinks and is a possible soft-lock
        # for health regen potion
        if self.our_hero.regen_timer > 0:
            regen = int(self.our_hero.max_hp * .2)
            self.our_hero.heal(regen)
            self.our_hero.regen_timer -= 1
        # for haste potion for 5 turn dodge increases
        self.our_hero.dodge = self.our_hero.base_dodge
        if self.our_hero.haste_timer > 0:
            centerprint('Your dodge chance is elevated')
            self.our_hero.haste_timer -= 1
        else:
            self.our_hero.dodge = self.our_hero.base_dodge
        self.our_hero.apply_equip()
        marqueeprint('[HERO TURN]')
        crit = 0
        crit_rand = random.randrange(0, 100)
        if crit_rand in range(self.our_hero.crit, crit_rand):
            crit = self.our_hero.atk * .4
        eff_atk = int(self.our_hero.atk + crit)
        if eff_atk < 0:
            eff_atk = 0
        if m == 'a' or m == '':
            if crit_rand == 0:
                centerprint('CRITICAL HIT!')
            self.our_enemy.damage(eff_atk + crit, self.our_hero.atk_curve)
            self.our_hero.our_weapon.damagedur(eff_atk + crit, self.our_hero.def_curve)
            if self.our_enemy.hp < 0:
                self.our_enemy.hp = 0
                self.our_hero.is_battling = False
            return False
        elif m == 'd':
            marqueeprint('[DEFENSE]')
            self.our_hero.defn += self.our_hero.defn * self.our_hero.def_curve
            return False
        elif m == 'r':
            marqueeprint('[RUN ATTEMPT]')
            rand = random.randrange(0, 4)
            if rand == 0:
                centerprint('you ran away')
                self.our_hero.is_battling = False
            else:
                centerprint('you can\'t run!')
            return False
        elif m == 'i':
            item_not_chosen = True
            while item_not_chosen:
                item_not_chosen = self.item_management()
            return False
        elif m == 'h':
            self.our_hero.heal_flip()
        input()  # Wait

    # One round of an enemy turn
    def enemy_turn(self) -> None:
        overunder = random.randrange(0, 20)
        if self.our_enemy.is_alive:
            marqueeprint('[ENEMY ATTACK]')
            if overunder == 0:
                self.our_enemy.anger()
            elif overunder == 1:
                self.our_enemy.weaker()
            elif overunder == 2:
                centerprint(str(self.our_enemy.name) + ' ran away!')
                self.our_enemy.hp = 0
                self.our_hero.is_battling = False
                return
            if overunder in range(3, self.our_hero.dodge):
                centerprint(str(self.our_enemy.name) + ' swings and misses!')
                return
            if self.our_hero.is_battling:
                eff_atk = int(self.our_enemy.atk)
                if eff_atk < 0:
                    eff_atk = 0
                self.our_hero.our_armor.damage_dur(eff_atk, self.our_hero.def_curve)
                self.our_hero.our_shield.damage_dur(eff_atk, self.our_hero.def_curve)
                self.our_hero.damage(eff_atk)

    def riddle(self) -> None:
        marqueeprint('[RIDDLE]')
        centerprint('The area gets quiet. The wind blows.')
        centerprint('A torn page lands in your grasp. It reads:')
        print('\n')
        # query database for a single random riddle
        self.conn.execute('SELECT * FROM riddles ORDER BY RANDOM() LIMIT 1' + ';')
        row = self.conn.fetchall()[0]
        our_riddle = [row[0], row[1]]
        wrap_string = textwrap.wrap(our_riddle[0], width=self.data_width)
        answer = str(our_riddle[1]).lower()
        for line in wrap_string:
            centerprint(line)
        centerprint('Speak the answer to the wind...')
        user_answer = input()
        if user_answer == '' and self.riddle_mode == 1:
            while user_answer == '':
                centerprint('Please answer the riddle.')
                user_answer = input()
                if self.debugging:
                    marqueeprint(f'{answer}, you cheater!')
        if similarstring(user_answer, answer) and user_answer != '':
            centerprint('You have successfully answered the riddle')
            centerprint('The answer was \"' + answer + '\"')
            centerprint('I present you with this:')
            self.our_hero.add_gold(self.our_hero.level * 44)
            self.our_hero.add_xp(self.our_hero.next_level * .17)
        else:
            centerprint('You Fail! Leave this place!')

    # fetch a new enemy that is at hero's level (for now...)
    def get_enemy(self) -> Enemy:
        self.conn.execute('SELECT * FROM enemies WHERE level = ' + str(self.our_hero.level) + ';')
        rows = self.conn.fetchall()
        new_enemy = random.choice(rows)

        # create random enemy name
        level_name = random.choice((rows[0][1], rows[1][1],
                                    rows[2][1], rows[3][1],
                                    rows[4][1]))
        # part of random name
        adjective = random.choice((rows[0][2], rows[1][2],
                                   rows[2][2], rows[3][2],
                                   rows[4][2]))
        # part of random name
        enemy_name = random.choice((rows[0][3], rows[1][3],
                                    rows[2][3], rows[3][3],
                                    rows[4][3]))
        # part of random name
        our_new_enemy = Enemy.Enemy(new_enemy[0], level_name, adjective, enemy_name, new_enemy[4],
                                    new_enemy[5], (new_enemy[6] + (new_enemy[6] * self.our_hero.def_curve)),
                                    new_enemy[7], new_enemy[8], new_enemy[9])
        return our_new_enemy

    # a blacksmith who can repair or sell gear
    def blacksmith(self):
        centerprint('An old Blacksmith rests at your camp')
        centerprint('He shows his wares and services:')
        centerprint('[f]ix gear [b]uy gear')
        next_decision = input()
        centerprint('Gold: ' + str(self.our_hero.gold))
        if next_decision == 'f':

            # offer equipment repair for any of the 3 slots, for 1g/durability point
            centerprint('The Blacksmith can offer repair ')
            centerprint('services for 1g/repair point')
            centerprint('Here is your gear durability:')

            # print all your gear out
            gridoutput(self.our_hero.ourweapon.datadict())
            gridoutput(self.our_hero.ourshield.datadict())
            gridoutput(self.our_hero.ourarmor.datadict())

            # user input for what to repair, or all of it, for convenience
            decision = input('What do you want to repair? [a] for all')
            if decision == '1' or decision == 'a':
                repair_cost = self.our_hero.ourweapon.maxdur - self.our_hero.ourweapon.dur
                centerprint('Repair Your weapon?')
                centerprint(f'Cost: {repair_cost} gold')
                centerprint('[y]es [n]o')
                decision2 = input()
                if decision2 == 'y' and self.our_hero.gold >= repair_cost:
                    self.our_hero.gold -= repair_cost
                    self.our_hero.ourweapon.dur = self.our_hero.ourweapon.maxdur
                    centerprint('Repair Success.')
            if decision == '2' or decision == 'a':
                repair_cost = self.our_hero.ourshield.max_dur - self.our_hero.ourshield.dur
                centerprint('Repair Your shield?')
                centerprint(f'Cost: {repair_cost} gold')
                centerprint('[y]es [n]o')
                decision2 = input()
                if decision2 == 'y' and self.our_hero.gold >= repair_cost:
                    self.our_hero.gold -= repair_cost
                    self.our_hero.ourshield.dur = self.our_hero.ourshield.max_dur
                    centerprint('Repair Success.')
            if decision == '3' or decision == 'a':
                repair_cost = self.our_hero.ourarmor.max_dur - self.our_hero.ourarmor.dur
                centerprint('Repair Your armor?)')
                centerprint(f'Cost: {repair_cost} gold')
                centerprint('[y]es [n]o')
                decision2 = input()
                if decision2 == 'y' and self.our_hero.gold >= repair_cost:
                    self.our_hero.gold -= repair_cost
                    self.our_hero.ourarmor.dur = self.our_hero.ourarmor.max_dur
                    centerprint('Repair Success')

        # offer random choice of weapon, armor, or shield at 1.5x value price
        elif next_decision == 'b':
            weapon_for_sale = self.our_hero.new_weapon()
            armor_for_sale = self.our_hero.new_armor()
            shield_for_sale = self.our_hero.new_shield()

            marqueeprint('[YOUR GEAR]')
            gridoutput(self.our_hero.ourweapon.datadict())
            gridoutput(self.our_hero.ourshield.datadict())
            gridoutput(self.our_hero.ourarmor.datadict())
            print('')

            # determine weapon costs
            wepcost = weapon_for_sale.level * 60 * self.our_hero.def_curve
            armcost = armor_for_sale.level * 60 * self.our_hero.def_curve
            shcost = shield_for_sale.level * 60 * self.our_hero.def_curve

            data1 = [str(weapon_for_sale.name), str(weapon_for_sale.type),
                     str(weapon_for_sale.baseatk),
                     str(wepcost)]
            data2 = [str(shield_for_sale.name), str(shield_for_sale.type),
                     str(shield_for_sale.base_defn),
                     str(shcost)]
            data3 = [str(armor_for_sale.name), str(armor_for_sale.type),
                     str(armor_for_sale.base_defn),
                     str(armcost)]

            title = '[GEAR FOR SALE]'
            dataheader = ['Name', 'Type', 'Atk/Def', 'Cost']
            alldata = [data1, data2, data3]
            fiverowprintoptions(dataheader, alldata, title)
            print('\n')
            centerprint('Please enter decision [ENTER] to go back')
            itemindex = input()
            if itemindex not in ['1', '2', '3', '']:
                centerprint('Please enter a valid choice')
            elif itemindex == '1':
                self.our_hero.ourweapon = weapon_for_sale
                if self.our_hero.gold < wepcost:
                    centerprint('You don\'t have enough money!')
                self.our_hero.gold -= wepcost
                centerprint('You equip your new gear: ' + str(weapon_for_sale.name) + ' ' + str(weapon_for_sale.type))
            elif itemindex == '2':
                self.our_hero.ourshield = shield_for_sale
                if self.our_hero.gold < wepcost:
                    centerprint('You don\'t have enough money!')
                    return
                self.our_hero.gold -= armcost
                centerprint('You equip your new gear: ' + str(shield_for_sale.name) + ' ' + str(shield_for_sale.type))
            elif itemindex == '3':
                self.our_hero.ourarmor = armor_for_sale
                if self.our_hero.gold < shcost:
                    centerprint('You don\'t have enough money!')
                    return
                self.our_hero.gold -= shcost
                centerprint('You equip your new gear: ' + str(armor_for_sale.name) + ' ' + str(armor_for_sale.type))
            self.our_hero.apply_equip()
            return

    # a camp where you regain hp after so many fights.
    def camp(self):
        camping = True
        while camping:
            self.our_hero.hp = self.our_hero.max_hp
            marqueeprint('[CAMP]')
            centerprint('You rest at camp. Hero HP: ' + str(self.our_hero.hp))
            centerprint('[a]dventure [i]tem [h]ero')
            centerprint('[p]eddler [b]lacksmith')
            centerprint('[l]oad [s]ave [q]uit')
            m = input()
            if m == 'i':
                iteming = True
                while iteming:
                    iteming = self.item_management()
            elif m == 'h':
                marqueeprint('[HERO DETAIL]')
                gridoutput(self.our_hero.datadict())
                input()  # Wait
                gridoutput(self.our_hero.our_weapon.datadict())
                input()  # Wait
                gridoutput(self.our_hero.our_shield.datadict())
                input()  # Wait
                gridoutput(self.our_hero.our_armor.datadict())
                input()  # Wait
            elif m == 'a' or m == '':
                return
                # adventure()
            elif m == 'l':
                marqueeprint('[LOAD GAME]')
                self.our_hero = self.load_game()
            elif m == 's':
                marqueeprint('[SAVE GAME]')
                self.savegame()
            elif m == 'b':
                marqueeprint('[BLACKSMITH]')
                self.blacksmith()
            elif m == 'p':
                marqueeprint('[PEDDLER\'S WARES]')
                self.peddler()
            elif m == 'q':
                marqueeprint('[QUIT]')
                decision = input('Are you sure?')
                if decision == 'y':
                    quit()
            else:
                centerprint('You walk back to camp')

    # sell the hero items (will be able to buy soon)
    def peddler(self):
        centerprint('An old Peddler rests at your camp.')
        centerprint('He shows his wares:')
        centerprint('[b]uy, [r]iddle (100g)')
        nextdecision = input()
        if nextdecision == 'b':
            pass
            item1 = self.our_hero.new_item()
            item2 = self.our_hero.new_item()
            item3 = self.our_hero.new_item()
            item4 = self.our_hero.new_item()
            item5 = self.our_hero.new_item()
            itemarray = [item1, item2, item3, item4, item5]
            for i, item in enumerate(itemarray):
                print(str(i + 1) + '\t' + item.name + '\t' + str(item.val * 1.5))
            print('Your selection? (ENTER to go back)')
            selection = input()
            if selection == '1':
                self.our_hero.buy_item(item1)
            elif selection == '2':
                self.our_hero.buy_item(item2)
            elif selection == '3':
                self.our_hero.buy_item(item3)
            elif selection == '4':
                self.our_hero.buy_item(item4)
            elif selection == '5':
                self.our_hero.buy_item(item5)
            elif selection == '':
                centerprint('\"WHYD YOU COME HERE AND NOT BUY ANYTHING?\"')
                return
            else:
                centerprint('Get out of here you bum!')
                # offer random choice of items at 1.5x value price
        if nextdecision == 'r':
            if self.our_hero.can_afford(100):
                self.our_hero.gold -= 100
                self.riddle()

    # pickle in to hero obj and start gameloop
    @staticmethod
    def load_game():
        # load hero object from pickle file
        dirlist = os.listdir('./saves/')
        for i, item in enumerate(dirlist):
            print(str(i) + ' - ' + str(item))
            print(str(datetime.datetime.fromtimestamp(os.path.getmtime('./saves/' + item))))
            print('\n')
        index = input("Which Character?\nOr [c]ancel")
        if index == '':
            index = 0
        if index == 'c':
            return
        index = int(index)
        ourpickle = open(('./saves/' + str(dirlist[index])), "rb")
        ourdata = pickle.load(ourpickle)
        return ourdata

    # pickle our hero to file
    def savegame(self):
        # pickle hero object to file
        # should prompt to overwrite
        hero_name = input('Name your save file\nOr [c]ancel')
        if hero_name == 'c':
            return
        save_directory = "./saves/"
        filepath = save_directory + hero_name + '.hero'
        game_data = self.our_hero
        if not os.path.isfile(filepath):
            with open(filepath, 'wb') as f:
                pickle.dump(game_data, f, -1)
        else:
            answer = input('Overwrite?')
            if answer.lower() == 'y':
                os.remove(filepath)
                print(os.listdir('./saves/'))
                with open(filepath, 'wb') as f:
                    pickle.dump(game_data, f, -1)
            elif answer.lower() == 'n':
                newname = input('Enter New Save file name')
                with open(filepath + str(newname), 'wb') as f:
                    pickle.dump(game_data, f, -1)

    # TODO: Go back from item menu without enemy turn happening
    # TODO: Make this into an item selection method, with an argument if [s]elling, [u]sing, or [d]iscarding
    # lets hero use items
    def item_management(self):
        if not self.our_hero.items:
            centerprint('Inventory Empty')
            return False
        # print all the item's info
        for i, item in enumerate(self.our_hero.items):
            leftprint('ITEM: ' + str(i + 1))
            gridoutput(self.our_hero.items[i].datadict())
        centerprint('Please enter decision, [ENTER] to go back')
        try:
            itemindex = input()
            itemindex = int(itemindex)
            itemindex -= 1
            self.our_hero.ouritem = self.our_hero.items[int(itemindex)]
            del (self.our_hero.items[int(itemindex)])
        except ValueError:
            centerprint('Please enter a valid choice')
            return False
        except IndexError:
            centerprint('Please enter a valid choice')
            return False
        self.our_hero.activeitem = self.our_hero.ouritem
        centerprint('Using ' + str(self.our_hero.ouritem.name))
        if self.our_hero.ouritem.name == 'Healing Potion':
            self.healing_potion()
        if self.our_hero.ouritem.name == 'Explosive Mana Vial':
            if self.our_hero.is_battling:
                self.explosive_mana_vial()
            else:
                centerprint('You\'re not in battle!')
                return False
        if self.our_hero.ouritem.name == 'Health Regen Potion':
            self.health_regen_potion()
        if self.our_hero.ouritem.name == 'Haste Potion':
            self.haste_potion()
        if self.our_hero.ouritem.name == 'Weapon Repair Tincture':
            self.weapon_repair_tincture()

    # hero uses a healing potion
    def healing_potion(self):
        marqueeprint('[HEALING POTION]')
        healed = self.our_hero.active_item.effect
        self.our_hero.heal(healed)
        self.our_hero.active_item = 0

    # hero uses an item that damages enemy
    def explosive_mana_vial(self):
        marqueeprint('[EXPLOSIVE MANA BOMB]')
        centerprint('The Mana Vial EXPLODES!')
        dmg = self.our_hero.active_item.effect
        self.our_enemy.damage(dmg, self.our_hero.atk_curve)
        self.our_hero.active_item = 0

    # adds health per turn
    def health_regen_potion(self):
        marqueeprint('[REGEN POTION]')
        self.our_hero.regen_timer += 5
        centerprint(str(self.our_hero.regen_timer) + ' turns health regen')
        self.our_hero.active_item = 0

    # dodge buff
    def haste_potion(self):
        marqueeprint('[HASTE POTION]')
        self.our_hero.haste_timer += 5
        centerprint(str(self.our_hero.haste_timer) + ' turns dodge buff')
        self.our_hero.active_item = 0

    # heals 60% of dur points to weapon
    def weapon_repair_tincture(self):
        marqueeprint('[WEAPON REPAIR]')
        rep = self.our_hero.our_weapon.maxdur * .6
        centerprint('You repaired your weapon for ' + str(rep) + ' durability points')
        self.our_hero.our_weapon.dur += rep
        if self.our_hero.our_weapon.dur > self.our_hero.our_weapon.maxdur:
            self.our_hero.our_weapon.dur = self.our_hero.our_weapon.maxdur
        self.our_hero.active_item = 0

    # adds a little suspense to offset the monotony of text input
    def suspense(self) -> None:
        s = ' '
        if self.suspense_mode:
            time.sleep(.5)
            print(s)

    # Print hero and enemy justified on left and right
    def print_adversaries(self, datawidth):
        self.text_width = datawidth
        centerprint(lr_justify('[HERO]', '[ENEMY]', self.text_width))
        centerprint(lr_justify(self.our_hero.name, self.our_enemy.name, self.text_width))
        centerprint(lr_justify(str('lvl: ' + str(self.our_hero.level)),
                               str('lvl: ' + str(self.our_enemy.level)), self.text_width))
        centerprint(lr_justify(str('HP: ' + str(self.our_hero.hp) + '/' + str(self.our_hero.max_hp)),
                               str('HP: ' + str(self.our_enemy.hp) + '/' + str(self.our_enemy.max_hp)), self.text_width))
        centerprint(lr_justify(str('XP: ' + str(self.our_hero.xp) + '/' + str(self.our_hero.next_level)),
                               str('XP drop: ' + str(self.our_enemy.xp)), self.text_width))

    # To be used on status screens
    def printmarqueehero(self, sometext):
        marqueeprint(sometext)
        print(lr_justify('[HERO]', '', self.text_width))
        print(lr_justify(self.our_hero.name, '', self.text_width))
        print(lr_justify(f'lvl: {self.our_hero.level}', '', self.text_width))
        print(lr_justify(f'HP: {self.our_hero.hp} / {self.our_hero.max_hp}', '', self.text_width))
        print(lr_justify(f'XP: {self.our_hero.xp} / {self.our_hero.next_level}', '', self.text_width))
