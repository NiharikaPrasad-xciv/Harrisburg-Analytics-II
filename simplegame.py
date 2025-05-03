# prompt: please create a game for me a simple one for dodge vlocks

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 10

# Enemy
enemy_size = 30
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = 0
enemy_speed = 5

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_y = 0
        enemy_x = random.randint(0, WIDTH - enemy_size)

    # Collision detection
    if player_x < enemy_x + enemy_size and player_x + player_size > enemy_x and \
            player_y < enemy_y + enemy_size and player_y + player_size > enemy_y:
        running = False  # Game Over

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_size, enemy_size))
    pygame.display.update()

    clock.tick(60)  # Frames per second

pygame.quit()
