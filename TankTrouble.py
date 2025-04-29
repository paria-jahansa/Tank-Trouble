# Random Maze Generator using Depth-first Search
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
# FB - 20121214
# Game features two tanks shooting each other inside the maze

import random
import math
import pygame
from PIL import Image
from pygame.math import Vector2

# Tank dimensions
tnkx = 26
tnky = 33

# Scores and control flags
score1 = 0
score2 = 0
s = 0
done = False
h = True
game = True

# Wall direction vectors for DFS maze generation
dx = [0, 0, 0, 1, 0, 1]
dy = [-1, 1, -1, -1, 0, 0]

# Load images for horizontal and vertical walls
ofoghImg = pygame.image.load('ofoghi.png')
amudImg = pygame.image.load('amudi.png')

# Main maze generation using DFS and pruning
def maze():
    a = random.randint(0, 1)
    # Choose whether to start with horizontal or vertical walls
    if a == 0:
        stack = [(random.randint(1, mx - 2), random.randint(1, my - 1), 0)]
    else:
        stack = [(random.randint(1, mx - 1), random.randint(1, my - 2), 1)]

    while len(stack) > 0:
        (cx, cy, a) = stack[-1]
        nlst = []  # List of valid neighbors

        if a == 0:  # Horizontal wall
            ofoghiMaze[cy][cx] = 1
            # Check two horizontal directions
            for i in range(2):
                nx = cx + dx[i]
                ny = cy + dy[i]
                if 0 < ny < my and ofoghiMaze[ny][nx] == 0:
                    ctr = 0
                    for j in range(2):
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if 0 < ey < my and ofoghiMaze[ey][ex] == 1:
                            ctr += 1
                    for j in [2,3,4,5]:
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if 0 < ex < mx and amudiMaze[ey][ex] == 1:
                            ctr += 1
                    if ctr < 3:
                        nlst.append((i, 0, 0))
            # Check vertical neighbors
            for i in [2,3,4,5]:
                nx = cx + dx[i]
                ny = cy + dy[i]
                if 0 < nx < mx and amudiMaze[ny][nx] == 0:
                    ctr = 0
                    for j in range(2):
                        ex = nx + dy[j]
                        ey = ny + dx[j]
                        if 0 < ex < mx and amudiMaze[ey][ex] == 1:
                            ctr += 1
                    for j in [2,3,4,5]:
                        ex = nx + dy[j]
                        ey = ny + dx[j]
                        if 0 < ey < my and ofoghiMaze[ey][ex] == 1:
                            ctr += 1
                    if ctr < 3:
                        nlst.append((i, 0, 1))

        elif a == 1:  # Vertical wall
            amudiMaze[cy][cx] = 1
            # Check horizontal neighbors
            for i in range(2):
                nx = cx + dy[i]
                ny = cy + dx[i]
                if 0 < nx < mx and amudiMaze[ny][nx] == 0:
                    ctr = 0
                    for j in range(2):
                        ex = nx + dy[j]
                        ey = ny + dx[j]
                        if 0 < ex < mx and amudiMaze[ey][ex] == 1:
                            ctr += 1
                    for j in [2,3,4,5]:
                        ex = nx + dy[j]
                        ey = ny + dx[j]
                        if 0 < ey < my and ofoghiMaze[ey][ex] == 1:
                            ctr += 1
                    if ctr < 3:
                        nlst.append((i, 1, 1))
            # Check vertical neighbors
            for i in [2,3,4,5]:
                nx = cx + dy[i]
                ny = cy + dx[i]
                if 0 < ny < my and ofoghiMaze[ny][nx] == 0:
                    ctr = 0
                    for j in range(2):
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if 0 < ey < my and ofoghiMaze[ey][ex] == 1:
                            ctr += 1
                    for j in [2,3,4,5]:
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if 0 < ex < mx and amudiMaze[ey][ex] == 1:
                            ctr += 1
                    if ctr < 3:
                        nlst.append((i, 1, 0))

        # Backtracking step
        if len(nlst) > 0:
            (ir, a, b) = nlst[random.randint(0, len(nlst) - 1)]
            if a == 0:
                cx += dx[ir]
                cy += dy[ir]
            else:
                cx += dy[ir]
                cy += dx[ir]
            stack.append((cx, cy, b))
        else:
            stack.pop()

# Draw horizontal wall
def ofogh(x, y):
    for ky in range(5):
        for kx in range(60):
            if x*60 + kx < imgx and y*60 + ky < imgy:
                pixels[x*60+kx, y*60+ky] = (0, 0, 0)
    gameDisplay.blit(ofoghImg, (x*60, y*60))
    if h:
        wall = Wall(x*60+3, y*60+1.25, 55, 2)
        ofoghiwall.add(wall)

# Draw vertical wall
def amud(x, y):
    for ky in range(60):
        for kx in range(5):
            if x*60 + kx < imgx and y*60 + ky < imgy:
                pixels[x*60+kx, y*60+ky] = (0, 0, 0)
    gameDisplay.blit(amudImg, (x*60, y*60))
    if h:
        wall = Wall(x*60+1.25, y*60+2.5, 2, 55)
        amudiwall.add(wall)

# Render entire maze from matrices
def showMaze(o, m, n, a):
    for i in range(m):
        for j in range(n-1):
            if o[i][j] == 0:
                ofogh(j, i)
        if i != m-1:
            for j in range(n):
                if a[i][j] == 0:
                    amud(j, i)
    h = False

# Tank class with movement and collision
class Player(pygame.sprite.Sprite):                     
    def __init__(self, t, m, image_path):
        super().__init__()                                              
        pos = (t, m)
        self.image = pygame.image.load(image_path)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        self.direction = Vector2(0, -1)
        self.speed = 0 
        self.angle_speed = 0
        self.angle = 0
        self.tir = 0  # Bullet count

    def update(self):
        # Rotate tank image and direction
        if self.angle_speed != 0:
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        old = [self.rect.x, self.rect.y]
        new = old + self.direction * self.speed
        self.rect.x = new[0]
        self.rect.y = new[1]

        # Wall collision check
        collide1 = pygame.sprite.spritecollide(self, amudiwall, False)
        collide2 = pygame.sprite.spritecollide(self, ofoghiwall, False)
        if collide1 or collide2:
            self.rect.x = old[0]
            self.rect.y = old[1]
            self.position = self.rect.center
        else:
            self.position += self.direction * self.speed
            self.rect.center = self.position

# Wall block class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0,255,255))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# Bullet logic including wall bounce
class Bullet(pygame.sprite.Sprite):
    def __init__(self, tank):
        super().__init__()
        self.tank = tank
        self.direction = Vector2(tank.direction)
        self.position = Vector2(
            tank.position[0] + (tnky / 2) * math.cos(math.atan2(tank.direction[1], tank.direction[0])),
            tank.position[1] + (tnky / 2) * math.sin(math.atan2(tank.direction[1], tank.direction[0]))
        )
        self.speed = 2.8
        self.image = pygame.Surface([6, 6])
        self.image.fill((160,160,160))
        pygame.draw.circle(self.image, (0,0,0), (3,3), 3, 0)
        self.time = 0
        self.count = 0
        self.rect = self.image.get_rect(center=self.position)
        self.old = [self.rect.x, self.rect.y]

    def update(self):
        # Bounce on vertical walls
        if pygame.sprite.spritecollide(self, amudiwall, False):
            self.direction[0] *= -1
        # Bounce on horizontal walls
        elif pygame.sprite.spritecollide(self, ofoghiwall, False):
            self.direction[1] *= -1
        self.position += self.direction * self.speed
        self.rect.center = self.position
        self.count += 1
        self.time = self.count // 60

        
        '''collide1 = pygame.sprite.spritecollide(self, amudiwall , False)
        collide2 = pygame.sprite.spritecollide(self, ofoghiwall , False)
        if collide1 or collide2:     
            self.rect.x = old[0]
            self.rect.y = old[1]
            self.position = self.rect.center
        else :
            self.position += self.direction * self.speed
            self.rect.center = self.position'''


pygame.init()
clock = pygame.time.Clock()
while not done:
    if game:
        s = 0                                           # who lost
        mx = random.randint(6, 20); my = random.randint(6, 10)
        imgx = mx*60; imgy = my*60
        image = Image.new("RGB", (imgx, imgy),(192,192,192))
        pixels = image.load()                                           
        ofoghiMaze = [[0 for x in range(mx)] for y in range(my+1)]
        amudiMaze = [[0 for x in range(mx+1)] for y in range(my)]
        maze()
        tank1 = pygame.image.load('tank1.png')
        tank2 = pygame.image.load('tank2.png')
        m = my+1
        n = mx+1
        xsize = 60*(n-1)+5
        ysize = 60*(m-1)+5
        gameDisplay = pygame.display.set_mode((xsize,ysize))
        tankx1 = random.randint(0, mx-1); tanky1 = random.randint(0, my-1)
        gameDisplay.blit(tank1, (tankx1*60+30,tanky1*60+30))
        player1 = Player(tankx1*60+30, tanky1*60+30,'tank1.png')
        tankx2 = random.randint(0, mx-1); tanky2 = random.randint(0, my-1)
        if tankx1!= tankx2 :
            gameDisplay.blit(tank2, (tankx2*60+30, tanky2*60+30))
            player2 = Player(tankx2*60+30, tanky2*60+30,'tank2.png')
        else :
            while tanky1==tanky2:
                tanky2 = random.randint(0, my-1)
            gameDisplay.blit(tank2, (tankx2*60+30, tanky2*60+30))
            player2 = Player(tankx2*60+30, tanky2*60+30,'tank2.png')
        amudiwall = pygame.sprite.Group()
        ofoghiwall = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        showMaze(ofoghiMaze,m,n,amudiMaze)
        
        playersprite1= pygame.sprite.RenderPlain(player1)
        playersprite2= pygame.sprite.RenderPlain(player2)
        all_sprites.add(playersprite1,playersprite2)
        image.save("background.png", "PNG")
        background = pygame.image.load('background.png')
        gameDisplay.blit(background,(0,0))
        pygame.display.set_caption('Tank Trouble')
        game = False
    clock.tick(60)                   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.speed = 2
            elif event.key == pygame.K_DOWN:
                player1.speed = -1
            elif event.key == pygame.K_LEFT:
                player1.angle_speed = -4
            elif event.key == pygame.K_RIGHT:
                player1.angle_speed = 4
            elif event.key == pygame.K_m:
                if player1.tir < 5 :
                    player1.tir +=1
                    bullet = Bullet(player1)
                    bullet.rect.x = player1.rect.x
                    bullet.rect.y = player1.rect.y
                    all_sprites.add(bullet)
                    bullet_list.add(bullet)
            if event.key == pygame.K_e:
                player2.speed = 2
            elif event.key == pygame.K_d:
                player2.speed = -1
            elif event.key == pygame.K_s:
                player2.angle_speed = -4
            elif event.key == pygame.K_f:
                player2.angle_speed = 4
            elif event.key == pygame.K_q:
                if player2.tir < 5 :
                    player2.tir +=1
                    bullet = Bullet(player2)
                    bullet.rect.x = player2.rect.x
                    bullet.rect.y = player2.rect.y
                    all_sprites.add(bullet)
                    bullet_list.add(bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1.angle_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player1.speed = 0
            if event.key == pygame.K_f or event.key == pygame.K_s:
                player2.angle_speed = 0
            elif event.key == pygame.K_e or event.key == pygame.K_d:
                player2.speed = 0
    for bullet in bullet_list:
        if bullet.time == 10:
            bullet.tank.tir -=1
            bullet_list.remove(bullet)
            all_sprites.remove(bullet)     
    for bullet in bullet_list:
        if pygame.sprite.spritecollide(bullet, [player1] , False) and bullet.count>6:
            all_sprites.remove(playersprite1) ; all_sprites.remove(bullet);game = True ; s = 1 ; score2 +=1
        if pygame.sprite.spritecollide(bullet, [player2] , False) and bullet.count>6:
            all_sprites.remove(playersprite2) ; all_sprites.remove(bullet);game = True ; s = 2 ; score1 +=1
    all_sprites.update()
    gameDisplay.blit(background,(0,0))
    all_sprites.draw(gameDisplay)      
    pygame.display.flip()
    if game:
        l = True
        gameDisplay.fill((255,255,204))
        #pygame.display.flip()
        font = pygame.font.Font(None,35)
        if s == 2:
            text1 = font.render('TANK 1 WINS!!', True, (255,0,127))
            gameDisplay.blit(text1, [imgx/4, imgy/5])
        if s == 1:
            text1 = font.render('TANK 2 WINS!!', True, (255,0,127))
            gameDisplay.blit(text1, [imgx/4, imgy/5])
        text2 = font.render('TANK 1 :', True, (51,51,255))
        gameDisplay.blit(text2, [imgx/4, 3*imgy/5])
        text3 = font.render('TANK 2 :', True, (255,51,51))
        gameDisplay.blit(text3, [imgx/4, 4*imgy/5])
        text4 = font.render(str(score1), True, (102,102,255))
        gameDisplay.blit(text4, [2*imgx/3, 3*imgy/5])
        text5 = font.render(str(score2), True, (255,102,102))
        gameDisplay.blit(text5, [2*imgx/3, 4*imgy/5])
        pygame.display.flip()
        while l :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True ; l = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    l = False


pygame.quit()

