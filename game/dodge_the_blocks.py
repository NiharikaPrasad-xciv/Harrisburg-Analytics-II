import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks - Advanced")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Player
player_size = 20
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 8

# Enemy
enemy_size = 50
enemy_list = []

# Power-up
power_up_radius = 15
power_up_list = []
power_up_timer = 0

# Game mechanics
score = 0
level = 1
high_score = 0
ENEMY_FALL_SPEED = 6
POWER_UP_DURATION = 300
shield_active = False
shield_timer = 0

# Load or initialize high score
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0
else:
    high_score = 0

def detect_collision(p, e):
    px, py = p
    ex, ey = e
    return (ex < px < ex + enemy_size or ex < px + player_size < ex + enemy_size) and \
           (ey < py < ey + enemy_size or ey < py + player_size < ey + enemy_size)

def spawn_enemies():
    if len(enemy_list) < 8:
        x_pos = random.randint(0, WIDTH - enemy_size)
        enemy_list.append([x_pos, 0])

def spawn_power_up():
    global power_up_timer
    if random.random() < 0.01 and power_up_timer == 0:
        x = random.randint(20, WIDTH - 20)
        y = 0
        power_up_list.append([x, y])
        power_up_timer = 500

def move_enemies():
    global score, level, ENEMY_FALL_SPEED
    for enemy in enemy_list[:]:
        enemy[1] += ENEMY_FALL_SPEED
        if enemy[1] > HEIGHT:
            enemy_list.remove(enemy)
            score += 1
            if score % 10 == 0:
                level += 1
                ENEMY_FALL_SPEED += 1

def move_power_ups():
    for power in power_up_list[:]:
        power[1] += 4
        if power[1] > HEIGHT:
            power_up_list.remove(power)

def draw_elements():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
    for power in power_up_list:
        pygame.draw.circle(screen, GREEN, (power[0], power[1]), power_up_radius)
    if shield_active:
        pygame.draw.circle(screen, YELLOW, (player_pos[0]+player_size//2, player_pos[1]+player_size//2), player_size, 2)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))
    screen.blit(high_score_text, (WIDTH//2 - 100, HEIGHT - 40))
    pygame.display.update()

def game_loop():
    global power_up_timer, shield_active, shield_timer, score, level, ENEMY_FALL_SPEED, high_score
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed

        spawn_enemies()
        spawn_power_up()
        move_enemies()
        move_power_ups()

        if power_up_timer > 0:
            power_up_timer -= 1

        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        for power in power_up_list[:]:
            dx = power[0] - (player_pos[0] + player_size // 2)
            dy = power[1] - (player_pos[1] + player_size // 2)
            if (dx ** 2 + dy ** 2) ** 0.5 < power_up_radius + player_size // 2:
                power_up_list.remove(power)
                shield_active = True
                shield_timer = POWER_UP_DURATION

        for enemy in enemy_list[:]:
            if detect_collision(player_pos, enemy):
                if shield_active:
                    enemy_list.remove(enemy)
                    shield_active = False
                else:
                    if score > high_score:
                        high_score = score
                        with open("highscore.txt", "w") as f:
                            f.write(str(high_score))
                    return  # Game Over

        draw_elements()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    game_loop()
