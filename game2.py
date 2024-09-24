import pygame
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('resources/background.png')

# Background Sound
mixer.music.load('resources/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Dodge the Enemies")
icon = pygame.image.load('resources/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('resources/player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
player_speed = 2  # Reduced speed

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemy_speed = 1  # Reduced speed for enemies

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('resources/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 550))
    enemyX_change.append(random.choice([-enemy_speed, enemy_speed]))
    enemyY_change.append(random.choice([-enemy_speed, enemy_speed]))

# Score
score_value = 0
font = pygame.font.Font('resources/Unlock-Regular.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('resources/Unlock-Regular.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def is_collision(playerX, playerY, enemyX, enemyY):
    distance = ((enemyX - playerX) ** 2 + (enemyY - playerY) ** 2) ** 0.5
    return distance < 40

# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
            if event.key == pygame.K_UP:
                playerY_change = -player_speed
            if event.key == pygame.K_DOWN:
                playerY_change = player_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Player Movement
    playerX += playerX_change
    playerY += playerY_change

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemy Movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]

        # Bounce enemies off the screen edges
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
        if enemyY[i] <= 0 or enemyY[i] >= 536:
            enemyY_change[i] = -enemyY_change[i]

        # Collision detection
        if is_collision(playerX, playerY, enemyX[i], enemyY[i]):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            running = False

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
