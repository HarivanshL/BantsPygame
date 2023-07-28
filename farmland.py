from state import State
from rect import Shape
from player import Player
from enemy import Enemy
import pygame
import random
import math

class FarmScreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.background = pygame.image.load("BACKGROUND_CITY.xcf")
        
       # self.screen = self.game.screen
        self.cropTypes = [ "MINT.xcf", "ROSE.xcf", "Lavender.xcf"]
        self.crops = ["Mint", "Rose", "Lavender"]
        self.types = []
        self.xLocation = []
        self.yLocation = []
        self.cropRects = []
        self.cropLocations = []
        self.img = ("doctor.xcf")
        self.size = 0
        self.radius = 10
        self.makeCrops(10)
        self.enemy = Enemy()
        self.enemy.makeEnemies(4, True)
        self.circlPosX = []
        self.circlePosY = []
        self.circleArray = []
        self.inInventory = False
        self.cropTimers = []
        self.enemyTimers = []
        self.enemyHitTimes = []
        self.maxCrops = 15
        self.ratCoins = []
        self.plantDrop = []
        self.font = pygame.font.SysFont(None, 30)
        self.coinimg = "COIN.xcf"

        #self.rect = pygame.Rect(50, 100, 50, 50)

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
            self.player = self.prev_state.player
            self.player.resetLocation(5, True)
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()
        self.player.resetLocation(1265, False)

    def update(self, actions):
        key = pygame.key.get_pressed()
        self.player.moveFarm(key, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)
        if self.player.rect.left < 1:
            self.inInventory = False
            self.exit_state()
        #if actions["q"]:
            #self.gathered()
        self.checkOverlap(actions)
        if actions["r"]:       
            if self.player.checkPotion() and self.player.health <= 66.6:
                self.player.addHealth()
                self.player.inventoryAmounts[list(self.player.inventory.keys()).index("Potion")] -= 1

        if actions["e"]:
            if self.inInventory:
                self.inInventory = False
            else:
                self.inInventory = True
        #if q_pressed:    
           # self.player.harvestPlant(self.cropLocations, self.types, self.crops, self.size)
            #self.harvest(self.player.rect.left +25, self.player.rect.top + 25)  
        self.game.actions["e"] = False
        self.game.actions["r"] = False
        if self.player.playerHealthStatus():
            self.game.gameOver()
            self.game.game_is_over = True

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.game.game_is_over = True
        #if self.game.game_is_over:
            #self.player.gameOver()

            #self.exit_state()
            #self.game.state_stack.pop()




    def render(self, display):
        display.fill((211,211,211))
        pygame.display.set_caption("BLACK PLAGUE CITY")
        display.blit(pygame.transform.scale(self.background, (1280, 720)), (0, 0))
        #pygame.draw.rect(screen, (0, 0, 255), self.rect)
        self.putCrops(display)
        self.enemy.putEnemies(display)
        #self.enemy.moveEnemies()
        #self.enemy.movenum2(self.player)
        #self.enemy.move_towards_player(self.player)
        ##FIX ME: MAKE LITTLE MAN RENDER AS DOCTOR2.XCF IF GOING RIGHT
        self.enemyMovement()
        self.player.draw(display, "doctor.xcf")
        self.player.displayHealth(self.game.screen)
        if self.inInventory:
            self.player.showInventory(display)
        #if self.size == 0:
            #self.resetCrops(display)

        #self.randomSpawnCrops()
        if len(self.ratCoins) > 0:
            self.renderRatDrop()
        if len(self.plantDrop) > 0:
            self.renderPlantDrop()
        
        #self.runFarm()



    def runFarm(self):
        if pygame.time.get_ticks() % 20000 <=  10:
            self.enemy.makeEnemies(2, False)
        if pygame.time.get_ticks() % 15000 <= 10:
            self.makeCrops(2)

    def makeCrops(self, size):
        for i in range(size):
            type = random.randint(0, 2)
            self.types.append(type)
            xx = random.randint(0, 1180)
            yy = random.randint(30, 620)
            self.xLocation.append(xx)
            self.yLocation.append(yy)
            self.cropRects.append(pygame.rect.Rect(xx, yy, 50, 50))
            self.cropLocations.append([xx, yy])
            self.size += 1

    def putCrops(self, display):
        for x in range(self.size):
            img_surface = pygame.image.load(self.cropTypes[self.types[x]]).convert_alpha()
            conformed = pygame.transform.scale(img_surface, (50, 50))
            display.blit(conformed, self.cropRects[x])

    def resetCrops(self, size):
        self.makeCrops(self, size)
        self.putCrops(self, self.game.screen)

    def checkOverlap(self, actions):
        for x in range(self.size):
            if self.cropRects[x].colliderect(self.player.getRect()):
                if actions["q"]:
                    xx = self.cropRects[x].x
                    yy = self.cropRects[x].y
                    img = self.cropTypes[self.types[x]]
                    self.plantDrop.append([xx, yy, pygame.time.get_ticks(), img])
                    self.cropRects.pop(x) 
                    self.player.addToInventory(self.crops[self.types[x]])
                    self.types.pop(x) #started going slow when i added this
                    self.size -= 1
                    self.cropTimers.append(pygame.time.get_ticks())
                break
        #for x in range(len(self.enemy.enemyRects)):
        index = 0
        for x in range(len(self.enemy.enemyRects)):
            if self.enemy.enemyRects[x].colliderect(self.player.getRect()):
                currentTime = pygame.time.get_ticks()/1000
            #if self.enemy.enemyRects[x].colliderect(self.player.getRect()):
            #FIXME
                #enemyHitTime = pygame.time.get_ticks() 
                if actions["q"]:
                    dropCoinChance = random.randint(0, 1)  
                    dropCoinChance = 1      
                    if (dropCoinChance == 1):
                        #changed
                        #self.dropCoin(x, self.game.screen)
                        xx = self.enemy.enemyRects[x].x
                        yy = self.enemy.enemyRects[x].y
                        self.ratCoins.append([xx, yy, pygame.time.get_ticks()])
                        self.player.increaseGold(5)

                    #self.enemy.enemyRects.pop(x) 
                    self.enemy.enemyRects.pop(x)
                    self.enemy.numEnemies -= 1
                    self.enemy.Locations.pop(x)
                    break
                else:
                    if not self.player.healthDecreasing:
                        self.player.healthDecreasing = True
                        self.player.lastTimePoisoned = pygame.time.get_ticks()
                    #self.player.slowlyKillPlayer(currentTime)
                    #self.enemy.enemySpawnTimes.append(pygame.time.get_ticks()
            #index +=1
    
    def enemyMovement(self):
#FIXME make movements less jagged
        for x in range(len(self.enemy.enemyRects)):
            x_distance = abs(self.player.rect.x - self.enemy.enemyRects[x].x)
            y_distance = abs(self.player.rect.y - self.enemy.enemyRects[x].y)
            if x_distance <= 300 and y_distance <= 300:
                self.enemy.move_towards_player(self.player, x)
            else:
                self.enemy.moveEnemiesRandom(x)


    def randomSpawnCrops(self):
#FIXME rat spawn location not to spawn on person
#FIXME screen slows down a lot
#FIXME list index outta range
        if self.size < self.maxCrops:
            xx = 1200
            yy = random.randint(100, 620)
            self.cropRects.append(pygame.rect.Rect(xx, yy, 50, 50))
            self.size +=1
            #self.cropTimers.pop(x)


#Crop class for the purpose of readability and easy access to deleting and putting crops
#FIXME fix the reset function to do it with time 

#woashee
#moving arround
#im in player making a hitting animation. what

    def other(self):
        #x or y
                x =3
                numero = random.randint(0, 1)
            #direction
                numerodos = random.randint(0, 1)
                if numero == 0:
                    if numerodos ==0:
                        self.enemy.enemyRects[x].left += 3
                        self.enemy.turned = False
                    else: 
                        self.enemy.enemyRects[x].left -= 3
                        self.enemy.turned = True
                else:
                    if numerodos == 0:
                        self.enemy.enemyRects[x].top += 3
                    else:
                        self.enemy.enemyRects[x].top -= 3

                if self.enemy.enemyRects[x].left < 0:
                    self.enemy.enemyRects[x].left = 0
                if self.enemy.enemyRects[x].right > 1280:
                    self.enemy.enemyRects[x].right = 1280
                if self.enemy.enemyRects[x].top < 0:
                    self.enemy.enemyRects[x].top = 0
                if self.enemy.enemyRects[x].bottom > 720:
                    self.enemy.enemyRects[x].bottom = 720  

    def renderFadingImage(self, x, y, screen, amount, img):
        text_surface = self.font.render("+" + str(amount), True, (0,0,0))
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (50, 50))
        text_rect.topleft = (x, y)
        img_surface = pygame.image.load(img).convert_alpha()
        coin_rect = pygame.rect.Rect(x, y, 100, 100)
        screen.blit(pygame.transform.scale(img_surface, (50, 50)), coin_rect)
        screen.blit(text_surface, text_rect)

    def renderRatDrop(self):
        for x in range(len(self.ratCoins)):
            if (pygame.time.get_ticks() - self.ratCoins[x][2])/1000 < 1:
                self.renderFadingImage(self.ratCoins[x][0], self.ratCoins[x][1], self.game.screen, 5, "COIN.xcf")
                self.ratCoins[x][1] -= 1
            else:
                self.ratCoins.pop(x)
                break

    def renderPlantDrop(self):
        for x in range(len(self.plantDrop)):
            if (pygame.time.get_ticks() - self.plantDrop[x][2])/1000 < 1:
                self.renderFadingImage(self.plantDrop[x][0], self.plantDrop[x][1], self.game.screen, 1, self.plantDrop[x][3])
                self.plantDrop[x][1] -= 1
            else:
                self.plantDrop.pop(x)
                break
