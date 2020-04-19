import pygame

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))
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


def player(x, y):
    screen.blit(playerImg, (x, y))


# Game Loop
pygame.key.set_repeat(25, 25)
running = True
while running:
    pygame.event.pump()
    screen.fill((0, 100, 200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                playerX -= playerX_change
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            playerX += playerX_change
        

    if (playerX <= 0):
        playerX = 0
    elif (playerX >= 736):
        playerX = 736
    player(playerX, playerY)
    pygame.display.update()
    

