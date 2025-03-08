import sqlite3

def get_monster_names():
    conn = sqlite3.connect("database/monsters.db")  # Adjust path if needed
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM monsters")  # Fetch only monster names
    monsters = cursor.fetchall()
    
    conn.close()
    
    return [monster[0] for monster in monsters]  # Extract names

if __name__ == "__main__":
    monster_names = get_monster_names()
    print("Monsters in Database:", monster_names)
