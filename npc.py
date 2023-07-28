import random
import pygame
from rect import Shape


class NPC():
    def __init__(self, rect, img, screen, game):
        self.rect = rect
        self.npc_x, self.npc_y, self.npc_w, self.npc_h = self.rect.x, self.rect.y, self.rect.w, self.rect.h
        self.img = img
        self.game = game
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.right = False
        self.left = False

        self.speed_x = 5
        self.speed_y = 4
        self.xdirectional = 1    
        self.ydirectional = 1  

        self.hasPendingQuest = False
        self.colliding = False
        self.medicines = ["Penecillin", "Electuary", "Ointment"]
        self.npcVoice = ""
        self.numOfMedicine = 0
        self.typeOfMedicine = ""
        self.generateNpcRequests()
        self.lastTimeMoved = pygame.time.get_ticks()
        self.lasty = 0
        self.lastx = 1
        self.targetLocationx = self.rect.x + 100
        self.targetLocationy = self.rect.y - 100
        self.startLocationX = self.rect.x +100
        self.startLocationY = self.rect.y +100
        self.direction = random.randint(0,1)
        self.y_directional = 1
        self.x_directional = 1
        self.moveable = True
        self.firstSpawn = 0

    def draw(self):
        img_surface = pygame.image.load(self.img).convert_alpha()
        self.screen.blit(img_surface, self.rect)

    def talk(self, voiceLine):
        text_surface = self.font.render(voiceLine, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.npc_x, self.npc_y-50)
        self.screen.blit(text_surface, text_rect)
    
    def checkIfHasRequests(self):
        if not self.hasPendingQuest:
            self.generateNpcRequests()
            self.hasPendingQuest = True
        self.showRequest()
    
    def questIsCompleted(self):
        self.hasPendingRequest = False
        self.checkIfHasRequests()
    
    def showBubbles(self, screen):
        pygame.draw.circle(screen, (175, 175, 175), (self.rect.x + 50 , self.rect.y - 50), 25)
        text_surface = self.font.render("...", True, self.BLACK)
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (100, 100))
        text_rect.topleft = (self.rect.x+40, self.rect.y - 70)
        self.screen.blit(text_surface, text_rect)

    def showRequest(self):
        Shape.drawRect(Shape, self.screen, self.rect.x + 25 , self.rect.y - 50, 150, 25, (175,175,175))
        text_surface = self.font.render(self.npcVoice, True, self.BLACK)
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (100, 100))
        text_rect.topleft = (self.rect.x+40, self.rect.y - 50)
        self.screen.blit(text_surface, text_rect)
        

    def generateNpcRequests(self):
        #generate number based on time in game
        num = 0
#FIXME lots of issues with this not working
        #mins = (pygame.time.get_ticks()- self.game.lastTimeGameIsOver)/60000 
        mins = (pygame.time.get_ticks())/60000 

        if mins <= 2:
            num = 1
        elif mins <= 4:
            num = 2
        else:
            num = 3

       # for x in range(3):
            #generate random medicinal item
        medicine = random.randint(0, 2)
        self.npcVoice = str(num) + self.medicines[medicine]
        self.numOfMedicine = num
        self.typeOfMedicine = self.medicines[medicine]


    def move(self):
        self.clock.tick(60)  
        
        #check x left
        if self.rect.left <= 0 + self.npc_w:
            self.xdirectional *= -1
            self.speed_x = abs(self.speed_x) * self.xdirectional
        #check x right
        if self.rect.right >= 1280 - self.npc_w:
            self.xdirectional *= -1
            self.speed_x = abs(self.speed_x) * self.xdirectional
        #check y top
        if self.rect.top <= 0 + self.npc_h:
            self.ydirectional *= -1
            self.speed_y = abs(self.speed_y) * self.ydirectional
        #check y bot
        if self.rect.bottom >= 720 - self.npc_h:
            self.ydirectional *= -1
            self.speed_y = abs(self.speed_y) * self.ydirectional

        self.rect.left += self.speed_x
        self.rect.top += self.speed_y
        self.npc_x += self.speed_x
        self.npc_y += self.speed_y

    def npcMovement(self):
        if self.direction:
            #move x
            if not(self.rect.x == self.startLocationX):
                self.rect.x += self.x_directional
            else:
                self.x_directional = -1 * self.x_directional
                self.startLocationX = self.startLocationX+ (100 * self.x_directional)
                self.direction = False
        else:
            #move y
            if not(self.rect.y == self.startLocationY):
                self.rect.y += 1 * self.y_directional
            else:
                self.y_directional =  -1* self.y_directional
                self.startLocationY = self.startLocationY+ (100 * self.y_directional)
                self.direction = True
