import sqlite3

# Connect to the database
def connect():
    return sqlite3.connect("database/monsters.db")

# CREATE TABLE: Ensure the monsters table exists
def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monsters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            health INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Table 'monsters' ensured to exist.")

# CREATE: Add a new monster (prevents duplicates)
def add_monster(name, monster_type, health, attack, defense):
    if monster_exists(name):
        print(f"⚠️ Monster '{name}' already exists!")
        return
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO monsters (name, type, health, attack, defense)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, monster_type, health, attack, defense))
    conn.commit()
    conn.close()
    print(f"✅ Monster '{name}' added successfully!")

# READ: Get all monsters
def get_all_monsters():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monsters")
    monsters = cursor.fetchall()
    conn.close()
    return monsters

# SEARCH: Find a monster by name
def search_monster_by_name(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monsters WHERE name LIKE ?", ('%' + name + '%',))
    monsters = cursor.fetchall()
    conn.close()
    return monsters

# SEARCH: Find monsters by type
def search_monster_by_type(monster_type):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monsters WHERE type = ?", (monster_type,))
    monsters = cursor.fetchall()
    conn.close()
    return monsters

# FILTER: Get monsters above a certain health value
def filter_monsters_by_health(min_health):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monsters WHERE health >= ?", (min_health,))
    monsters = cursor.fetchall()
    conn.close()
    return monsters

# UPDATE: Update a monster’s stats
def update_monster(monster_id, name, monster_type, health, attack, defense):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE monsters 
        SET name = ?, type = ?, health = ?, attack = ?, defense = ? 
        WHERE id = ?
    ''', (name, monster_type, health, attack, defense, monster_id))
    conn.commit()
    conn.close()
    print(f"✅ Monster ID {monster_id} updated successfully!")

# DELETE: Remove a monster
def delete_monster(monster_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM monsters WHERE id = ?", (monster_id,))
    conn.commit()
    conn.close()
    print(f"🗑️ Monster ID {monster_id} deleted successfully!")

# DELETE ALL: Reset the database (USE CAREFULLY)
def delete_all_monsters():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM monsters")
    conn.commit()
    conn.close()
    print("⚠️ All monsters have been deleted!")

# CHECK: See if a monster already exists
def monster_exists(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monsters WHERE name = ?", (name,))
    monster = cursor.fetchone()
    conn.close()
    return monster is not None

# RUN SCRIPT: Create table and insert sample monsters
if __name__ == "__main__":
    create_table()  # Ensure table exists before adding monsters
    
    # Add sample monsters (prevents duplicate errors)
    add_monster("Drakon", "Fire", 100, 30, 20)
    add_monster("AquaSerpent", "Water", 120, 25, 15)
    add_monster("TerraBeast", "Earth", 150, 40, 30)

    # Print all monsters to confirm insertion
    print("\n📜 All Monsters in Database:")
    for monster in get_all_monsters():
        print(monster)

    # Uncomment below to reset the database
    # delete_all_monsters()
