import pygame
import random
import math

# Initialize pygame
pygame.init()
score = 0

# Create screen
screen = pygame.display.set_mode((800, 600))

#Images
background = pygame.image.load("./img/background.png")  # Background
bullet = pygame.image.load("./img/bullet.png")  # bullet
icon = pygame.image.load("./img/battleship.png")

# Title and Icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("./img/space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 5
playerY_change = 5

# Enemy
enemyImg = pygame.image.load("./img/enemy.png")
enemyX = random.randint(0,736) #Randomize enemy position
enemyY = random.randint(50, 150)  # Randomize enemy position
enemyX_change = 5
enemyY_change = 5

# Bullet
#States: READY - Can't see it; FIRE - In flight
bulletImg = pygame.image.load("./img/bullet.png")
bulletX = 0 #Temp val - will use Player's X later on
bulletY = 480  
bulletX_change = 5 #Not used -- bullets don't change X coordinates
bulletY_change = 10
bullet_state = "READY"

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                         (math.pow(enemyY - bulletY, 2)))
    if (distance < 27):
        return True

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemyDestroyed():
    global enemyX
    global enemyY
    enemyX = random.randint(0,736) #Randomize enemy position
    enemyY = random.randint(50, 150)  # Randomize enemy position

def enemy(x, y):
    screen.blit(enemyImg, (x, y)) 

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "FIRE"
    screen.blit(bulletImg, (x+16,y+10)) #Make bullet appear on center of ship

# Game Loop
pygame.key.set_repeat(25, 25)
running = True
while running:
    pygame.event.pump()
    screen.fill((0, 0, 0)) #fill default black background -> will be covered by image
    #Add Background Image
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                playerX -= playerX_change
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            playerX += playerX_change
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if (bullet_state is "READY"):
                bulletX = playerX #Grab X value for bullet start point
                fire_bullet(bulletX, playerY)

    #Bullet Movement
    if (bulletY <= 0):
        bulletY = 480
        bullet_state = "READY"
    if (bullet_state is "FIRE"):
        fire_bullet(bulletX, bulletY) #Use bullet start X coordinate
        bulletY -= bulletY_change



    # Check player bounds
    if (playerX <= 0):
        playerX = 0
    elif (playerX >= 736):
        playerX = 736
    

    enemyX += enemyX_change
    # Check Enemy bounds
    if (enemyX <= 0):
        enemyX_change = 5
        enemyY += enemyY_change
    elif (enemyX >= 736):
        enemyX_change = -5
        enemyY += enemyY_change

    #Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if (collision):
        bulletY = 480
        bullet_state = "READY"
        score += 100
        print(f"Score: {score}")
        enemyDestroyed()

    player(playerX, playerY)
    enemy(enemyX, enemyY)




    pygame.display.update()
    

