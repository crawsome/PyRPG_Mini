# PyRPG_Mini

A text RPG written in Python 3 with many technical RPG features you'd want.
## Requirements / Dependencies
* Python3
* sqlite3
* textwrap
* time
* pickle
* os
* datetime
* difflib
* random
* Read/write access to the project folder for database creation, reading, and saved games.

## Quick Preview

![](https://i.imgur.com/YTx0ZGj.gif)

## Game Features

* OOP Python RPG with simple class names, convenient calls like *ourhero.heal()* and *ourhero.isalive()*
* 15 levels of stats, weapons, items, and monsters
* 3 hero classes, each with unique gear and base stats, which makes them all a unique experience.
* Save / Load system for saving your character's progress
* A customizable set of CSVs for modifying the game , and creating your own turn-based RPG.
* A database population module which implements new changes and makes a new database. (Schema changes coming soon)
* 5 buyable, findable, usable items with added status effects (damage, healing, regen, dodge, weapon repair)

## What you will experience
* Randomized battle system ensuring a fun grinding and leveling experience. Later levels require more effort, gear, items.
* 75 enemies with different HP, XP, Gold, Atk, Def
* A miserable old traveler who gives unsolicited life advice
* A Blacksmith who sells and repairs gear
* Riddles which reward gold and EXP
* A Store which sells items

Check back soon for new features!

# How to use

0. For your convenience, you can skip any prompt and default \[n]ew game, \[w]arrior, \[1] easy, \[a]dventure, \[a]ttack by simply pressing \[enter].

 1. Run \_\_init\_\_.py. If the database was deleted, it will reload the database from the CSVs in ./csv/ folder.
 2. Press \[ENTER] to play regular game. Enter \[1] to go into debugging mode.
 3. Select \[n]ew game
 4. Choose your class: \[w]arrior \[m]age \[h]unter
 5. Choose difficulty: \[1]easy \[2]med \[3]hard
 6. Enter your character's name
 7. \[a]dventure or \[c]amp
 8. \[a]dventure will be a random choice of a battle, item, riddle, traveler.
 9. \[c]amp will regerate your health, and offer features like: \[a]dventure, \[i]tem, \[h]ero, \[p]eddler, \[b]lacksmith, \[l]oad, \[s]ave, \[q]uit
 10. Battle will give you several battle commands: \[a]tk, \[d]ef, \[r]un, \[i]tem, \[c]oinflip to \[h]eal (100g)
 11. Upon finishing a battle, you are rewarded with gold and exp.
 12. Have fun!

# Saving / loading
If loading game run game.py, and select \[l]oad when prompted.

If saving, go to camp, select \[s]ave, and name the save file. (The script needs permissions to write to the directory!)

# If you liked it:

[Contribute](https://colinburke.com/contribute), so I can dedicate more time to projects like this.

# About the Author

https://linkedin.com/in/colingburke
