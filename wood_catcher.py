import pygame
import random
import time

red = (238, 59, 59)
black = (0, 0, 0)
green = (127, 255, 0)
blue = (0, 255, 255)

pygame.init()
pygame.display.set_caption('Wood catcher')
screen_width = 500
screen_height = 480
win = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
FPS = 45
score = 0
scores = []
lost = False
vel = 2
high_score = 0

man_pic = pygame.image.load('assets_woodc/man.png')
bg = pygame.image.load('assets_woodc/bg.jpg')
brick_pic = pygame.image.load('assets_woodc/brick.png')
font = pygame.font.SysFont('comicsans', 30, True)
hsfile = 'assets_woodc\score.txt'


class Man(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 8
        self.width = 64
        self.height = 64

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(man_pic, (self.x, self.y))


class Brick(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(brick_pic, (self.x, self.y))

    def move(self):
        self.y += vel


def redrawWin():
    win.blit(bg, (0, 0))
    man.draw(win)
    score_text = font.render('Score: ' + str(score), 1, black)
    win.blit(score_text, (350, 10))
    highscore_text = font.render('Highscore: ' + str(high_score), 1, red)
    win.blit(highscore_text, (10, 10))

    if lost:
        scores.append(score)
        lost_text = font.render('You lost!', 1, red)
        win.blit(lost_text, (200, 100))
    for brick in bricks:
        brick.draw(win)
    pygame.display.update()


turn = 0
man = Man(200, 400)
run = True
bricks = []
goes = 0
while run:
    hisc = ""
    with open(hsfile, 'r') as hs:
        for line in hs:
            hisc = line
    high_score = hisc
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and man.x < screen_width - 64:
        man.x += man.vel
    elif keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
    ranx = 2
    ran = random.randrange(1, ranx)
    x = random.randrange(0, (screen_width - 64))
    if turn == 35:
        for i in range(ran):
            turn = 0
            bricks.append(Brick(x, 0))
            ranx += 1
    for brick in bricks:
        brick.move()
        if man.getRect().colliderect(brick.getRect()):
            bricks.pop(bricks.index(brick))
            score += 1
        elif brick.getRect().y >= screen_height:
            scores.append(score)
            if max(scores) > int(hisc):
                high_score = max(scores)
            with open(hsfile, 'w') as hs:
                hs.write(str(high_score))
            bricks.pop(bricks.index(brick))
            bricks.clear()
            lost = True
            score = 0
    redrawWin()
    man.getRect()
    if lost:
        time.sleep(2)
        lost = False
        vel = 2
    turn += 1
    vel += 0.001
pygame.quit()
