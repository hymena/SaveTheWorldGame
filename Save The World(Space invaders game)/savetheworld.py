import pygame, sys, random
from pygame.locals import *
from COLORS import *

FPS = 30  # Frames per seconds
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 500
BACKGROUND = CYAN
shooterImg = pygame.image.load("images/shooter.png")
pygame.init()  # Init the pygame
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Set the window size
pygame.display.set_caption("Shooting Game")  # Set the window title
FPSCLOCK = pygame.time.Clock()  # The Fps clock which makes the game slower or faster
shooter_x = 250
shooter_y = 750
meteorSpeed = 1
spaceShipSpeed = 5
EnemyList = []
BulletList = []
score = 0
boomSound = pygame.mixer.Sound("musics/boom.wav")
gunShotSound = pygame.mixer.Sound("musics/gunshot.wav")
pygame.mixer.music.load("musics/background.mp3")
pygame.mixer.music.play(-1, 0.0)
bg = pygame.image.load("images/bg.jpg")
once = 0
run = True
fontObj = pygame.font.Font("freesansbold.ttf", 16)


def shooter(x, y):
    WINDOW.blit(shooterImg, (x, y))


def collide(bullet, enemy):
    global score
    if enemy.rect.colliderect(bullet.rect):
        BulletList.remove(bullet)
        EnemyList.remove(enemy)
        score += 100
        del enemy
        del bullet


def gameOver():
    global run
    gameOverText = fontObj.render("Game over.Your score: " + str(score) + " Click anywhere to quit", True, BLACK)
    gameOverRect = gameOverText.get_rect()
    gameOverRect.center = (250, 400)
    WINDOW.blit(gameOverText, gameOverRect)
    pygame.display.update()
    while True:
        ev = pygame.event.wait()
        if (ev.type == QUIT) or (ev.type == MOUSEBUTTONDOWN):
            run = False
            break


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/meteor.png")
        self.rect = self.image.get_rect(topleft=(self.x - 15, self.y - 20))

    def drawEnemy(self):
        WINDOW.blit(self.image, (self.x, self.y))

    def moveEnemy(self):
        global run
        if self.y >= 750:
            gameOver()
        else:
            self.y += meteorSpeed
            self.rect.top += meteorSpeed


class Bullets:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/missile.png")
        self.rect = self.image.get_rect(topleft=(self.x - 7, self.y - 9))

    def drawBullet(self):
        WINDOW.blit(self.image, (self.x, self.y))

    def moveBullet(self):
        if self.y <= 0:
            BulletList.remove(self)
            del self
        else:
            self.y -= spaceShipSpeed
            self.rect.top -= spaceShipSpeed



while run:
    once += 10
    WINDOW.blit(bg, (0, 0))
    shooterRect = shooterImg.get_rect()
    scoreTextSurface = fontObj.render("Score: " + str(score), True, ORANGE)
    textRect = scoreTextSurface.get_rect()
    textRect.center = (450, 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_LEFT:
                if shooter_x >= 25:
                    shooter_x -= 15
            if event.key == pygame.K_RIGHT:
                if shooter_x <= 425:
                    shooter_x += 15
    if once % 1000 == 0:
        randomEnemyX = random.randint(60, 440)
        enemy = Enemy(randomEnemyX, -37)
        EnemyList.append(enemy)
    for enemy in EnemyList:
        enemy.drawEnemy()
        enemy.moveEnemy()
    if once % 500 == 0:
        bullet = Bullets(shooter_x + 19, shooter_y)
        gunShotSound.play()
        BulletList.append(bullet)
    for bullet in BulletList:
        bullet.moveBullet()
        bullet.drawBullet()

    for bullet in BulletList:
        for enemy in EnemyList:
            collide(bullet, enemy)

    shooter(shooter_x, shooter_y)
    WINDOW.blit(scoreTextSurface, textRect)
    pygame.display.update()
    FPSCLOCK.tick(FPS)


sys.exit()

