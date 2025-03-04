import os
import random
import sqlite3
import pygame
import sys

# Fix sound issues in WSL2
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

pygame.init()
pygame.mixer.init()

# Try loading attack sound safely
try:
    attack_sound = pygame.mixer.Sound("assets/attack.wav")
except pygame.error as e:
    print(f"Warning: Sound failed to load ({e})")
    attack_sound = None  # Prevents crashes if sound is missing

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

# Buttons
attack_button = pygame.Rect(50, 400, 200, 50)
special_button = pygame.Rect(300, 400, 200, 50)

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
def shake_screen():
    for _ in range(5):
        screen.fill(WHITE)
        pygame.display.update()
        pygame.time.delay(50)

# Player chooses a monster
def choose_monster():
    monsters = get_monsters()
    if not monsters:
        print("⚠️ No monsters found in database!")
        pygame.quit()
        sys.exit()

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

# Battle system with attack choices
def battle():
    player_monster = choose_monster()
    enemy_monsters = [m for m in get_monsters() if m != player_monster]

    if not enemy_monsters:
        print("⚠️ No enemy monsters available!")
        pygame.quit()
        sys.exit()

    enemy_monster = random.choice(enemy_monsters)

    player_hp, max_player_hp = player_monster[3], player_monster[3]
    enemy_hp, max_enemy_hp = enemy_monster[3], enemy_monster[3]

    running = True
    player_turn = True

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
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # Draw attack buttons
        pygame.draw.rect(screen, GREEN, attack_button)
        pygame.draw.rect(screen, BLUE, special_button)
        draw_text("Attack (Normal)", attack_button.x + 30, attack_button.y + 15, WHITE)
        draw_text("Attack (Powerful)", special_button.x + 30, special_button.y + 15, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                if attack_button.collidepoint(event.pos):  # Normal Attack
                    damage = max(1, player_monster[4] - enemy_monster[5])
                    enemy_hp -= damage
                    print(f"⚔️ {player_monster[1]} dealt {damage} damage!")
                    if attack_sound:
                        attack_sound.play()
                    shake_screen()
                    player_turn = False
                elif special_button.collidepoint(event.pos):  # Powerful Attack
                    damage = max(1, int(player_monster[4] * 1.5) - enemy_monster[5])
                    enemy_hp -= damage
                    print(f"🔥 {player_monster[1]} used a powerful attack! Dealt {damage} damage!")
                    if attack_sound:
                        attack_sound.play()
                    shake_screen()
                    player_turn = False

        # Enemy turn (random attack)
        if not player_turn and enemy_hp > 0:
            pygame.time.delay(1000)
            enemy_damage = max(1, enemy_monster[4] - player_monster[5])
            player_hp -= enemy_damage
            print(f"💥 {enemy_monster[1]} attacked! Dealt {enemy_damage} damage!")
            if attack_sound:
                attack_sound.play()
            shake_screen()
            player_turn = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    battle()
