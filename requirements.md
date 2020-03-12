# Software Requirements Specifications for Spring 2020 "Software Engineering" PyRPG at Wright State University

## Overview


## References


## Functional Requirements

### [User Story A](features.md "Ref. Features and User Stories")

Req. 1.0 (Caleb): The modified app shall include a web-app that incorporates the game 

Req. 1.0.1 (Caleb): The modified app shall include a web-app shell that incorporates the Flask python web framework

Req. 1.0.2 (Caleb): The modified app shall include a web-app that implements the console portion of the game into the web application

Req. 1.0.3 (Caleb): The modified web-app will need to be styled to be visually appealing

Req. 1.1 (Caleb): The modified app’s web-app shall include a documentation page explaining how to play the game

### [User Story B](features.md "Ref. Features and User Stories")

Req: 2.0 (Nour): The modified app shall incorporate puzzle mini-games, including a descrambling game and a Caesar Cipher game.

Req. 2.1 (Nour): The modified app shall incorporate a descrambling puzzle mini-game for the player to complete to gain XP.

Req. 2.1.1 (Nour): Each word in the descramble will come from a large dictionary of words.

Req. 2.1.2 (Nour): The modified app shall provide the user with a hint to the answer upon their request, but this will decrease the amount of XP awarded.

Req. 2.2 (Nour): The modified app shall incorporate a Caesar Cipher puzzle mini-game for the player to complete to gain XP.

Req. 2.2.1 (Nour): Each word that is ciphered will come from a large dictionary of words.

Req. 2.2.2 (Nour): The modified app shall provide the user with a hint to the answer upon their request, but this will decrease the amount of XP awarded.

Req. 2.3 (Nour): Each of these games will be incorporated into the campsite of the main game.
 
### [User Story C](features.md "Ref. Features and User Stories")

Req. 3.0 (Anthony): The modified app shall have additional playable character classes beyond the base playable classes of Warrior, Mage, and Hunter.

Req. 3.1 (Anthony): The modified app shall have an information section available from the loading menu with a section dedicated to the playable character classes.

Req. 3.1.1 (Anthony): The informational section specific to character classes shall detail the differences, both positive and negative, of each playable character class. 

Req. 3.1.2 (Anthony): The playable character class information shall be stored in the database for a centralized way to update the information.

Req. 3.2 (Anthony): The playable character class Archer shall be added, bringing its own set of items.

Req. 3.2.1 (Anthony): The Archer class shall introduce a new set of Armor of varying levels, names, types, and stats, all stored in the database.

Req. 3.2.2 (Anthony): The Archer class shall introduce a new set of Shields of varying levels, names, types, and stats, all stored in the database.

Req. 3.2.3 (Anthony): The Archer class shall introduce a new set of Weapons of varying levels, names, types, and stats, all stored in the database.

Req. 3.2.4 (Anthony): The Archer class shall introduce a new set of Hero Perks found in Hero.py

Req. 3.3 (Anthony): The playable character class Monk shall be added, bringing its own set of items.

Req. 3.3.1 (Anthony): The Monk class shall introduce a new set of Armor of varying levels, names, types, and stats, all stored in the database.

Req. 3.3.2 (Anthony): The Monk class shall introduce a new set of Shields of varying levels, names, types, and stats, all stored in the database.

Req. 3.3.3 (Anthony): The Monk class shall introduce a new set of Weapons of varying levels, names, types, and stats, all stored in the database.

Req. 3.3.4 (Anthony): The Monk class shall introduce a new set of Hero Perks found in Hero.py

Req. 3.4 (Anthony): The playable character class Barbarian shall be added, bringing its own set of items.

Req. 3.4.1 (Anthony): The Barbarian class shall introduce a new set of Armor of varying levels, names, types, and stats, all stored in the database.

Req. 3.4.2 (Anthony): The Barbarian class shall introduce a new set of Shields of varying levels, names, types, and stats, all stored in the database.

Req. 3.4.3 (Anthony): The Barbarian class shall introduce a new set of Weapons of varying levels, names, types, and stats, all stored in the database.

Req. 3.4.4 (Anthony): The Barbarian class shall introduce a new set of Hero Perks found in Hero.py

Req. 3.5 (Andrew): The playable character class Assassin shall be added, bringing its own set of items.

Req. 3.5.1 (Andrew): The Assassin class shall introduce a new set of Armor of varying levels, names, types, and stats, all stored in the database.

Req. 3.5.2 (Andrew): The Assassin class shall introduce a new set of Shields of varying levels, names, types, and stats, all stored in the database.

Req. 3.5.3 (Andrew): The Assassin class shall introduce a new set of Weapons of varying levels, names, types, and stats, all stored in the database.

Req. 3.5.4 (Anthony): The Assassin class shall introduce a new set of Hero Perks found in Hero.py

### [User Story D](features.md "Ref. Features and User Stories")

Req. 4.0 (Andrew): The modified app shall provide an autosave feature than can be toggled on/off by the user.

Req. 4.0.1 (Andrew): The autosave feature will only save the game progress when the user returns to the main camp screen.

### [User Story E](features.md "Ref. Features and User Stories")

Req. 5.0 (Anthony): The modified game shall include an information printout with a list of information important to the player.
Req. 5.0.1 (Anthony): The printout shall include information detailing the flow of the game, including combat and the different types of random encounters. 

Req. 5.0.2 (Anthony): The printout shall include information detailing differences between hero classes.

Req. 5.0.3 (Anthony): The printout shall include information detailing the saving and loading game states. 

Req. 5.0.4 (Anthony): The printout shall include information detailing differences in items such as methods of obtaining them.

Req. 5.1 (Anthony): The information provided in the printout shall be stored in a text file for a centralized way to update the info.

### [User Story F](features.md "Ref. Features and User Stories")

Req. 6.0 (Anthony): The modified game shall have both open issues resolved.

Req. 6.1 (Anthony): The modified game shall ensure every menu has the same width.

Req. 6.2 (Anthony): The modified game shall ensure proper control of flow, for example, buying at the blacksmith should send you back to blacksmith instead of camp. 

Req. 6.3 (Anthony): The modified game shall ensure input is correctly validated. 

### [User Story G](features.md "Ref. Features and User Stories")

Req 7.0 (Andrew): The modified app shall have an expanded inventory management system to allow the user to store items and equipment acquired in the game.

Req 7.0.1 (Andrew): The user must have the option to store, equip or discard equipment found while adventuring.. 

Req 7.1 (Andrew): The inventory management system will have appropriate actions according to the item; use, equip, details and drop. 

Req 7.1.1 (Andrew): When prompted, the inventory system will display information about the selected item. 
