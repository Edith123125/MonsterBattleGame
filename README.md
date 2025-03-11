# MonsterBattleGame

Welcome to **Monster Battle Game**, a turn-based battle game where players choose a monster and fight against a randomly selected enemy monster! The game features animated attacks, attack sounds, and screen effects for an engaging experience.

## Features
- **Turn-based combat** between player and AI-controlled monsters.
- **Database-powered monster selection** with stats like health, attack, and defense.
- **Dynamic attack animations** with screen shake and flash effects.
- **sound effects** for normal and powerful attacks.

## Requirements
To run the game, you need:
- **Python 3**- language.
- **pygame** -library
- **SQLite**- for database

### Install Dependencies
Ensure you have the required dependencies installed:

pip install pygame

## How to Play
 -**Run the game** using the command:
   python src/battle.py
 - **Choose Your Monster**: Use `UP` and `DOWN` arrow keys to navigate and `ENTER` to select.
- **Battle Phase**:
   - Click on "Attack (Normal)" or "Attack (Powerful)" to strike your opponent.
   - The battle continues until one monster's health reaches zero.
 **Winning**: The game announces the winner and then exits.

## Folder Structure
MonsterBattleGame/
├── src/
│   ├── database.py    # Main game script
├── assets/
│   ├── attack_normal.wav
│   ├── attack_powerful.wav
│   ├── monsters/
│       ├── TerraBeast.png
│       ├── bazenga.png
│       ├── Drakon.png
│       ├── AquaSerpent.png
│       ├── ThunderBeast.png
│       ├── ShadowFang.png
│       ├── placeholder.png
├── database/
│   ├── monsters.db    
└── README.md          

### Author:Edith Gatwiri Kobia
Feel free to reach out if you have any feedback or would like to connect . github:https://github.com/

Enjoy the battle! ⚔️🔥

