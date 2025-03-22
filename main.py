import pygame
from pygame import mixer
import random
import math

pygame.init()


screen = pygame.display.set_mode((800, 600))


mixer.music.load("background.wav")
mixer.music.play(-1)


background = pygame.image.load('background_.png')



pygame.display.set_caption("Cosmos Invader")

icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)




playerImg = pygame.image.load('player.png')

playerX = 370
playerY = 480 





def player(x, y):
    screen.blit(playerImg, (x, y))




# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = 370
enemyY = 150
enemyX_change = 4
enemyY_change = 40
num_of_enemies = 6



def enemy(x, y):
    screen.blit(enemyImg, (x, y))




# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False





# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Game Loop
running = True
while running:

    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        playerX += 5
    elif keys[pygame.K_LEFT]:
        playerX -= 5
    elif keys[pygame.K_SPACE]:
        if bullet_state is "ready":
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.play()
            # Get the current x cordinate of the spaceship
            bulletX = playerX
            fire_bullet(bulletX, bulletY)



    if playerX <= 0:
        playerX = 0
    elif playerX >=800-64:
        playerX = 800-64





    # Game Over
    if enemyY > 440:
        enemyY = 2000
        game_over_text()
        break


    # Enemy Movement

    enemyX += enemyX_change
    
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        enemyY += enemyY_change
            # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        explosionSound = mixer.Sound("explosion.wav")
        explosionSound.play()
        bulletY = 480
        bullet_state = "ready"
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    enemy(enemyX, enemyY)


    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    pygame.display.update()



pygame.quit()
