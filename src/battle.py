import os
import random
import sqlite3
import pygame
import sys

# Fix sound issues in WSL2
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

pygame.init()
pygame.mixer.init()

# Try loading attack sounds safely
try:
    attack_sound_normal = pygame.mixer.Sound("assets/attack_normal.wav")
    attack_sound_powerful = pygame.mixer.Sound("assets/attack_powerful.wav")
except pygame.error as e:
    print(f"Warning: Sound failed to load ({e})")
    attack_sound_normal = None
    attack_sound_powerful = None

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Battle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Font
font = pygame.font.Font(None, 36)

# Database connection
def connect():
    return sqlite3.connect("database/monsters.db")

# Get all monsters
def get_monsters():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, health, attack, defense FROM monsters")
    monsters = cursor.fetchall()
    conn.close()
    return monsters

# Load monster images safely
def load_monster_image(name):
    path = f"assets/monsters/{name}.png"
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), (100, 100))  
    
    placeholder_path = "assets/monsters/placeholder.png"
    if os.path.exists(placeholder_path):
        print(f"Warning: Image for {name} not found. Using placeholder.")
        return pygame.transform.scale(pygame.image.load(placeholder_path), (100, 100))

    print(f"Error: No image found for {name} and no placeholder exists! Exiting.")
    pygame.quit()
    sys.exit()

# Display text on screen
def draw_text(text, x, y, color=BLACK):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Draw health bars
def draw_health_bar(x, y, current_hp, max_hp):
    bar_width = 200
    bar_height = 20
    fill_width = int((current_hp / max_hp) * bar_width)
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, fill_width, bar_height))

# Shake screen effect
def screen_shake():
    for _ in range(10):
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.fill(WHITE)
        pygame.display.update()
        pygame.time.delay(30)

# Flash effect when hit
def flash_effect():
    for _ in range(3):
        screen.fill(RED)
        pygame.display.update()
        pygame.time.delay(50)
        screen.fill(WHITE)
        pygame.display.update()
        pygame.time.delay(50)

# Animate attack movement
def animate_attack(attacker_x, attacker_y, attacker_img):
    for _ in range(5):
        screen.fill(WHITE)
        screen.blit(attacker_img, (attacker_x + 10, attacker_y))  
        pygame.display.update()
        pygame.time.delay(50)

    for _ in range(5):  
        screen.fill(WHITE)
        screen.blit(attacker_img, (attacker_x, attacker_y))  
        pygame.display.update()
        pygame.time.delay(50)

# Draw projectile effect
def draw_projectile(start_x, start_y, end_x, end_y, color):
    for i in range(10):
        progress = i / 10
        x = int(start_x + (end_x - start_x) * progress)
        y = int(start_y + (end_y - start_y) * progress)
        pygame.draw.circle(screen, color, (x, y), 10)
        pygame.display.update()
        pygame.time.delay(50)

# Player chooses a monster
def choose_monster():
    monsters = get_monsters()

    if not monsters:
        print("No monsters found in the database.")
        pygame.quit()
        sys.exit()

    selected_index = 0
    running = True

    while running:
        screen.fill(WHITE)
        draw_text("Choose Your Monster (Press UP/DOWN, ENTER to select):", 50, 50, BLUE)

        for i, monster in enumerate(monsters):
            color = GREEN if i == selected_index else BLACK
            draw_text(f"{monster[1]} (Type: {monster[2]}, HP: {monster[3]}, ATK: {monster[4]}, DEF: {monster[5]})", 100, 100 + i * 40, color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(monsters)
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(monsters)
                if event.key == pygame.K_RETURN:
                    return monsters[selected_index]

# Battle system
def battle():
    player_monster = choose_monster()
    monsters_list = get_monsters()
    possible_enemies = [m for m in monsters_list if m[0] != player_monster[0]]
    
    if not possible_enemies:
        pygame.quit()
        sys.exit()

    enemy_monster = random.choice(possible_enemies)
    player_hp, max_player_hp = player_monster[3], player_monster[3]
    enemy_hp, max_enemy_hp = enemy_monster[3], enemy_monster[3]

    player_image = load_monster_image(player_monster[1])
    enemy_image = load_monster_image(enemy_monster[1])

    running = True
    player_turn = True

    while running:
        screen.fill(WHITE)
        draw_text(f"Your Monster: {player_monster[1]}", 50, 50, GREEN)
        draw_health_bar(50, 80, player_hp, max_player_hp)
        draw_text(f"Enemy Monster: {enemy_monster[1]}", 50, 200, RED)
        draw_health_bar(50, 230, enemy_hp, max_enemy_hp)

        screen.blit(player_image, (400, 80))
        screen.blit(enemy_image, (400, 230))

        pygame.draw.rect(screen, GREEN, (50, 400, 200, 50))
        pygame.draw.rect(screen, BLUE, (300, 400, 200, 50))
        draw_text("Attack (Normal)", 70, 415, WHITE)
        draw_text("Attack (Powerful)", 320, 415, WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                if attack_sound_normal:
                    attack_sound_normal.play()
                animate_attack(400, 80, player_image)
                draw_projectile(400, 100, 400, 230, RED)
                screen_shake()
                enemy_hp -= max(1, player_monster[4] - enemy_monster[5])
                player_turn = False

        if not player_turn and enemy_hp > 0:
            pygame.time.delay(1000)
            if attack_sound_powerful:
                attack_sound_powerful.play()
            animate_attack(400, 230, enemy_image)
            draw_projectile(400, 230, 400, 80, BLUE)
            screen_shake()
            player_hp -= max(1, enemy_monster[4] - player_monster[5])
            player_turn = True

        if player_hp <= 0 or enemy_hp <= 0:
            winner = player_monster[1] if player_hp > 0 else enemy_monster[1]
            draw_text(f"{winner} wins the battle!", 50, 300, BLACK)
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    battle()
