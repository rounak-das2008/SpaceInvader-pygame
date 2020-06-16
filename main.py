import pygame
import random
from pygame import mixer


# Initialize the pygame -------
pygame.init()

# Create th screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background sounds
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship2.png')
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 18

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('space-invaders.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(30)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0  # Actually will not be used
bulletY_change = 13
bullet_state = 'ready'

# Ready -- can't be seen on screen but is readyto be fired
# Fired  -- bullet is fired


# Score -------
# score = 0

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)

textX = 10
textY = 10

# Game Over Text -----
# over_font = pygame.font.Font('freesansbold.ttf', 70)
over_font = pygame.font.SysFont("comicsansms.ttf", 200)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 100, 170))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(over_text, (335, 273))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    dis = (enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2
    distance = pow(dis, 0.5)
    if distance < 27:
        return True
    else:
        return False


# Game loop----
running = True

while running:
    # RGB -----
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke pressed then do these -----

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print('Left key has been pressed')
                playerX_change = -4

            elif event.key == pygame.K_RIGHT:
                # print('Right key has been pressed')
                playerX_change = 4

            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')         # Bullet firing sound------
                    bullet_sound.play()
                    # Get the current x coordinate of the bullet----
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print('Key released')
                playerX_change = 0

    # Checking for boundaries ----

    # Spaceship -------------
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy ---------------
    for i in range(num_of_enemies):

        # Game Over -----
        if enemyY[i] > 340:                     # 340
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            show_score(350, 300)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision ------------
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')  # Explosion sound-----
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            # print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement ----

    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    show_score(textX, textY)

    pygame.display.update()
