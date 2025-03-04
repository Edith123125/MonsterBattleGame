import os
import random
import sqlite3
import pygame
import sys
import time

# Fix audio issues in WSL
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

pygame.init()
pygame.mixer.init()

# Load attack sound safely
try:
    attack_sound = pygame.mixer.Sound("assets/attack.wav")
except pygame.error:
    print("⚠️ Warning: Sound failed to load.")
    attack_sound = None  # Prevent crash

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
    cursor.execute("SELECT id, name, type, health, attack, defense, speed FROM monsters")
    monsters = cursor.fetchall()
    conn.close()
    return monsters

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

# Player chooses a monster
def choose_monster():
    monsters = get_monsters()
    selected_index = 0
    running = True

    while running:
        screen.fill(WHITE)
        draw_text("Choose Your Monster (Press UP/DOWN, ENTER to select):", 50, 50, BLUE)

        for i, monster in enumerate(monsters):
            color = GREEN if i == selected_index else BLACK
            draw_text(f"{monster[1]} (Type: {monster[2]}, HP: {monster[3]})", 100, 100 + i * 40, color)

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

# Real-time battle system
def battle():
    player_monster = choose_monster()
    enemy_monster = random.choice([m for m in get_monsters() if m != player_monster])

    player_hp, max_player_hp = player_monster[3], player_monster[3]
    enemy_hp, max_enemy_hp = enemy_monster[3], enemy_monster[3]

    player_speed = player_monster[6]
    enemy_speed = enemy_monster[6]

    running = True
    last_attack_time = 0
    attack_cooldown = 1.5  # 1.5 seconds cooldown between attacks

    while running:
        screen.fill(WHITE)

        # Display monsters and health bars
        draw_text(f"Your Monster: {player_monster[1]}", 50, 50, GREEN)
        draw_health_bar(50, 80, player_hp, max_player_hp)

        draw_text(f"Enemy Monster: {enemy_monster[1]}", 50, 200, RED)
        draw_health_bar(50, 230, enemy_hp, max_enemy_hp)

        if player_hp <= 0 or enemy_hp <= 0:
            winner = player_monster[1] if player_hp > 0 else enemy_monster[1]
            draw_text(f"{winner} wins the battle!", 50, 300, BLACK)
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
            sys.exit()

        # Check attack cooldown
        current_time = time.time()
        if current_time - last_attack_time > attack_cooldown:
            if player_speed >= enemy_speed:
                enemy_hp -= max(1, player_monster[4] - enemy_monster[5])
            else:
                player_hp -= max(1, enemy_monster[4] - player_monster[5])
            last_attack_time = current_time
            if attack_sound:
                attack_sound.play()

        pygame.display.flip()
        pygame.time.delay(50)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    battle()
