import pygame
import sqlite3

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Battle - Menu System")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Database connection
def connect():
    return sqlite3.connect("database/monsters.db")

# Fetch all monsters from database
def get_monsters():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, health, attack, defense FROM monsters")
    monsters = cursor.fetchall()
    conn.close()
    return monsters

# Add a new monster
def add_monster(name, monster_type, health, attack, defense):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO monsters (name, type, health, attack, defense) VALUES (?, ?, ?, ?, ?)", 
                   (name, monster_type, health, attack, defense))
    conn.commit()
    conn.close()

# Delete a monster
def delete_monster(monster_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM monsters WHERE id = ?", (monster_id,))
    conn.commit()
    conn.close()

# Update a monster’s stats
def update_monster(monster_id, health, attack, defense):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE monsters SET health = ?, attack = ?, defense = ? WHERE id = ?", 
                   (health, attack, defense, monster_id))
    conn.commit()
    conn.close()

# Menu options
OPTIONS = ["View Monsters", "Add Monster", "Update Monster", "Delete Monster", "Exit"]
selected_option = 0  # Tracks which menu option is selected

def main_menu():
    global selected_option
    running = True

    while running:
        screen.fill(WHITE)

        # Display menu options
        for i, option in enumerate(OPTIONS):
            color = GREEN if i == selected_option else BLACK
            text = font.render(option, True, color)
            screen.blit(text, (100, 100 + i * 50))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(OPTIONS)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        view_monsters()
                    elif selected_option == 1:
                        add_monster_screen()
                    elif selected_option == 2:
                        update_monster_screen()
                    elif selected_option == 3:
                        delete_monster_screen()
                    elif selected_option == 4:
                        running = False

        pygame.display.flip()

    pygame.quit()

# Function to display monsters
def view_monsters():
    monsters = get_monsters()
    running = True

    while running:
        screen.fill(WHITE)
        y_offset = 50
        for monster in monsters:
            text = font.render(f"{monster[0]}. {monster[1]} ({monster[2]}) - HP: {monster[3]}", True, BLACK)
            screen.blit(text, (50, y_offset))
            y_offset += 40

        text = font.render("Press ESC to return", True, RED)
        screen.blit(text, (50, HEIGHT - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()

# Function to add a monster
def add_monster_screen():
    name = input("Enter monster name: ")
    monster_type = input("Enter monster type (Fire/Water/Earth): ")
    health = int(input("Enter health points: "))
    attack = int(input("Enter attack power: "))
    defense = int(input("Enter defense power: "))

    add_monster(name, monster_type, health, attack, defense)
    print(f"Monster {name} added successfully!")

# Function to delete a monster
def delete_monster_screen():
    monsters = get_monsters()
    if not monsters:
        print("No monsters available to delete.")
        return

    print("\nAvailable Monsters to Delete:")
    for monster in monsters:
        print(f"{monster[0]}. {monster[1]} ({monster[2]})")

    monster_id = int(input("Enter the ID of the monster to delete: "))
    delete_monster(monster_id)
    print(f"Monster ID {monster_id} deleted successfully!")

# Function to update a monster
def update_monster_screen():
    monsters = get_monsters()
    if not monsters:
        print("No monsters available to update.")
        return

    print("\nAvailable Monsters to Update:")
    for monster in monsters:
        print(f"{monster[0]}. {monster[1]} ({monster[2]})")

    monster_id = int(input("Enter the ID of the monster to update: "))
    health = int(input("Enter new health points: "))
    attack = int(input("Enter new attack power: "))
    defense = int(input("Enter new defense power: "))

    update_monster(monster_id, health, attack, defense)
    print(f"Monster ID {monster_id} updated successfully!")

if __name__ == "__main__":
    main_menu()
