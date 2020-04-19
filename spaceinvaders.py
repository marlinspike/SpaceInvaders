import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render(f"Score : {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


#Game Over Message
def game_over():
    over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    


# Create screen
screen = pygame.display.set_mode((800, 600))

#Images
background = pygame.image.load("./img/background.png")  # Background
bullet = pygame.image.load("./img/bullet.png")  # bullet
icon = pygame.image.load("./img/battleship.png")

#Sound
mixer.music.load('./wav/background.wav')
mixer.music.play(-1)

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
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("./img/enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(50)
#enemyImg = pygame.image.load("./img/enemy.png")
#enemyX = random.randint(0,736) #Randomize enemy position
#enemyY = random.randint(50, 150)  # Randomize enemy position
#enemyX_change = 5
#enemyY_change = 5

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

def enemyDestroyed(index):
    global enemyX
    global enemyY
    enemyX = random.randint(0,736) #Randomize enemy position
    enemyY = random.randint(50, 150)  # Randomize enemy position

def enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y)) 

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
                bullet_sound = mixer.Sound('./wav/laser.wav')
                bullet_sound.play()
                bulletX = playerX #Grab X value for bullet start point
                fire_bullet(bulletX, playerY)

    #Bullet Movement
    if (bulletY <= 0):
        bulletY = 480
        bullet_state = "READY" #Reset bullet, since it exited the screen
    if (bullet_state is "FIRE"):
        fire_bullet(bulletX, bulletY) #Use bullet start X coordinate
        bulletY -= bulletY_change

    # Check player bounds
    if (playerX <= 0):
        playerX = 0
    elif (playerX >= 736):
        playerX = 736
    
    # Enemy Movement
    for i in range(num_of_enemies):
        #Game Over Code
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  #Move enemies off screen
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if (enemyX[i] <= 0):
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif (enemyX[i] >= 736):
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if (collision):
            collision_sound = mixer.Sound('./wav/explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "READY"
            score_value += 100
            #print(f"Score: {score_value}")
            enemyX[i] = random.randint(0, 736)  # Randomize enemy position
            enemyY[i] = random.randint(50, 150)  # Randomize enemy position
        
        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    

