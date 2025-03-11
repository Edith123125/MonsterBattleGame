
import sqlite3
# this establishes database connection
def connect():
    return sqlite3.connect("database/monsters.db")
# adds the speed column
def add_speed_column():
    conn = connect()
    cursor = conn.cursor()
    
    try:
        # Checks if the column of the 'speed' already exists
        cursor.execute("PRAGMA table_info(monsters);")
        columns = [column[1] for column in cursor.fetchall()]
       # add speed column. 
        if "speed" not in columns:
            cursor.execute("ALTER TABLE monsters ADD COLUMN speed INTEGER DEFAULT 10;")
            conn.commit()
            print("✅ 'speed' column added successfully!")
        else:
            print("⚠️ 'speed' column already exists.")
# handles errors.
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    add_speed_column()
