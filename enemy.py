import pygame
import random
import math

class Enemy():
    def __init__(self):
        self.x = 50
        self.y = 50
       # self.screen_w = w
       # self.screen_h = h
        player_w, player_h = 50, 50
        self.rect = pygame.rect.Rect(30, 30, player_w, player_h)
        self.numEnemies = 0
        self.Locations =[]
        self.enemyRects = []
        self.img = "CITY_RAT.xcf"
        self.imgFlipped = "CITY_RAT_FLIPPED.xcf"
        self.distance = 0
        self.speed = 1.5
        self.enemySpawnTimes = []
        self.turned = False
        self.firstSpawn = 0
        self.maxEnemies = 10
        self.enemyTargets = []
        



    def makeEnemies(self, num, beginnning):
        for enemy in range(num):
            xx =0
            if beginnning:
                xx = random.randint(100, 1100)
            else:
                xx = 1200
            yy = random.randint(100, 620)
            self.enemyRects.append(pygame.rect.Rect(xx, yy, 50, 50))
            self.Locations.append([xx, yy, 50, 50])
            self.numEnemies +=1
            self.enemyTargets.append([xx, yy])
            #self.generateNewSpot(enemy)
            
        #self.firstSpawn = pygame.time.get_ticks()

    
    def randomSpawnEnemies(self):
#FIXME rat spawn location not to spawn on person
#FIXME screen slows down a lot
        if self.numEnemies < self.maxEnemies:
            print("out")
            xx = 1200
            yy = random.randint(100, 620)
            self.enemyRects.append(pygame.rect.Rect(xx, yy, 50, 50))
            self.Locations.append([xx, yy, 50, 50])
            self.numEnemies +=1
                #self.enemySpawnTimes.pop(x)
    
    def putEnemies(self, screen):
        for enemy in range(self.numEnemies):
            if self.turned:
                img_surface = pygame.image.load(self.imgFlipped).convert_alpha()
            else:
                img_surface = pygame.image.load(self.img).convert_alpha()
            screen.blit(img_surface, self.enemyRects[enemy])    
        
    def isOver(self, screen):
        if self.numEnemies == 0:
            text_surface = self.font.render("YOU WIN", True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (1280/2, 720/2)
            self.screen.blit(text_surface, text_rect)

    def move_towards_player(self, player, num):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.getRect().left - self.enemyRects[num].x, player.getRect().top - self.enemyRects[num].y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.enemyRects[num].x += dx * self.speed 
        self.enemyRects[num].y += dy * self.speed

    
    def generateNewSpot(self, x):
        xx = random.randint(0, 1200)
        yy = random.randint(0, 670)
        self.enemyTargets[x] = [xx, yy]
        print(self.enemyTargets[x])

    def moveEnemiesRandom(self,x):
        dx, dy = self.enemyTargets[x][0] - self.enemyRects[x].x, self.enemyTargets[x][1] - self.enemyRects[x].y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
        else:
            print("f")
            self.generateNewSpot(x)
        # Move along this normalized vector towards the player at current speed.
        self.enemyRects[x].x += dx * self.speed
        self.enemyRects[x].y += dy * self.speed




        
#FIXME rat damages
#FIXME only sometimes rats give gold
#FIXME animation for coin addition