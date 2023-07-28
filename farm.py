import pygame
import random
from player import Player
from rect import Shape

class Farm:   

    def __init__(self):
        self.xLocation = []
        self.yLocation = []
        self.size = 10
        self.radius = 10

    def runFarm(self, screen, peewee, key):
        clock = pygame.time.Clock()
        clock.tick(60)

        
        background = pygame.image.load("farmBackground.jpeg")
        #//#player.move(key)
        screen.fill((0, 255, 255)) 
        screen.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))
        peewee.draw(screen, ("monster.xcf"))  
        peewee.move(key, 1280, 720)
        self.putCrops(Farm, screen)
        #self.harvest(Farm, screen, peewee, key)

            
    def makeCrops(self):
        for i in range(self.size):
            self.xLocation.append(random.randint(0, 1280))
            self.yLocation.append(random.randint(0, 720))

           
    def putCrops(self, screen):
        for x in range(self.size):
            Shape.drawCircle(Shape, screen, (255,255,255), (self.xLocation[x], self.yLocation[x]), self.radius)

    def harvest(self, screen, peewee, key):
        for x in range(self.size):
            if key[pygame.K_q] and abs(Player.getX(peewee) -self.xLocation[x]) <= 11 and abs(Player.getY(peewee) - self.yLocation[x]) <= 11:
                self.xLocation.pop(x)
                self.yLocation.pop(x)
                self.size -= 1
