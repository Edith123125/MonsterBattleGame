import sqlite3

def get_monster_names():
    conn = sqlite3.connect("database/monsters.db")  # you can adjust path if needed
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM monsters")  # this fetches the monster names only. 
    monsters = cursor.fetchall()
    
    conn.close()
    
    return [monster[0] for monster in monsters]  

if __name__ == "__main__":
    monster_names = get_monster_names()
    print("Monsters in Database:", monster_names)
