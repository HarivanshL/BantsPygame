from state import State
from rect import Shape
from player import Player
from farmland import FarmScreen
import pygame
from npc import NPC


import random
from enemy import Enemy
import time
import math

class Main(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.TIMER_EVENT = pygame.event.custom_type()
        self.currentx = 0
        self.currenty = 0
        self.game = game
        self.SCREEN_WIDTH =1280
        self.background = pygame.image.load("BACKGROUND.xcf")
        self.show = False
        self.player = Player(game)
        self.img = ("doctor.xcf")
        self.xlocation = [100, 250, 400] #keeps track of locations
        self.npcVoiceLines =["beware the rats", "please im hungry", "this might be my last day.."]
        self.enemies = Enemy()
        self.bing = False
        self.atMarket = False
        self.atBrew = False
        self.marketActions = {"itemOne": False, "itemTwo": False, "itemThree": False}
        self.inInventory = False
        self.table = {"first" : False, "second" : False, "third" : False}
        self.npcRects = [pygame.Rect(100, 520, 100, 100), pygame.Rect(300, 520, 100, 100), pygame.Rect(820, 520, 100, 100)]
        self.npc1 = NPC(self.npcRects[0], "NPC1.xcf", self.game.screen, game)
        self.npc2 = NPC(self.npcRects[1], "NPC2.xcf", self.game.screen, game)
        self.npc3 = NPC(self.npcRects[2], "NPC3.xcf", self.game.screen, game)   
        self.npcs = [self.npc1, self.npc2, self.npc3]
        self.brewQueue = []
        self.timers = []
        self.medicines = ["medicine1.xcf", "medicine2.xcf", "Ointment.xcf"]
        self.medicines1 = ["Penecillin", "Electuary", "Ointment"]

        self.temps = []
        self.currentlyBrewing = False

        #market purposes
        #images of items       
        self.img_surface1 = pygame.image.load("medicine3.xcf").convert_alpha()
        self.img_surface2 = pygame.image.load("Potion.xcf").convert_alpha()
        self.img_surface3 = pygame.image.load("Honey.xcf").convert_alpha()
        self.rect1 = pygame.rect.Rect(1280/2 -250, 720/2, 100, 100)
        self.rect2 = pygame.rect.Rect(1280/2 - 50, 720/2, 100, 100)
        self.rect3 = pygame.rect.Rect(1280/2 + 150, 720/2, 100, 100)
        self.itemPrices = [10, 5, 15]
        self.marketList = {"Vinegar": self.itemPrices[0], "Potion": self.itemPrices[1], "Honey": self.itemPrices[2]}
        self.marketListItems = ["Vinegar", "Potion", "Honey"]
        self.itemLocations = [self.rect1, self.rect2, self.rect3]
        self.itemSelected = [False, False, False]

        self.coinimg = "COIN.xcf"
        self.font = pygame.font.SysFont(None, 30)
        self.images = ["Honey.xcf", "Potion.xcf", "medicine3.xcf", "Lavender.xcf", "ROSE.xcf", "MINT.xcf", "medicine1.xcf", "medicine2.xcf", "Ointment.xcf"]
        self.recipeImages = ["medicine1gray.xcf", "medicine2gray.xcf", "Ointment.xcf"]
        self.recipeNames = ["Penecillin", "Electuary", "Ointment"]

        self.recipeIngredientsDisplay = {"Penecillin": ["Vinegar", "Rose", "Lavender"], "Electuary": ["Honey", "Mint", "Lavender"], "Ointment": ["Vinegar", "Honey", "Lavender"]}
        self.recipeIngredientsAmounts = [[2, 1, 3], [2, 3, 4], [3, 2, 2]]  #[[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        self.recipeIngredientsImages = [["medicine3.xcf", "ROSE.xcf", "Lavender.xcf"], ["Honey.xcf", "MINT.xcf", "Lavender.xcf"], ["medicine3.xcf", "Honey.xcf", "Lavender.xcf"]]
        self.recipeIngredients = ["Ointment X 1\nMint X 5\n Lavender X 1\nRose X 1", "Honey X 1\nLavender X 4\n Rose X 2", "Honey x 2\nMint X 3\nRose X 3"]
        self.recipeIngredients2 = ["Ointment X 1\nMint X 5\n Lavender X 1\nRose X 1", "Honey X 1\nLavender X 4\n Rose X 2", "Honey x 2\nMint X 3\nRose X 3"]
        self.recipeIngredients3 = ["Ointment X 1\nMint X 5\n Lavender X 1\nRose X 1", "Honey X 1\nLavender X 4\n Rose X 2", "Honey x 2\nMint X 3\nRose X 3"]
        self.brewing = False
        self.mainscreenClock = pygame.time.Clock()
        self.lastClickedInvetory = 0
        self.lastClickedBrew = 0
        self.lastClickedMarket = 0
        self.brewPopUP = 0
        self.marketPopUP = 0
        self.coinPopUP = 0
        self.coinLocation = 30
        self.coins = []
        self.ingredients = []
        self.questsCompleted = []

    def update(self, actions):
        key = pygame.key.get_pressed()
        if actions["q"]:       
            self.player.hitting = True 
        if actions["r"]:       
            if self.player.checkPotion() and self.player.health < 100:
                self.player.addHealth()
                self.player.inventoryAmounts[list(self.player.inventory.keys()).index("Potion")] -= 1
        if not(self.atMarket or self.atBrew):
            self.player.moveMain(key, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT, self.xlocation, self.npcs)
         
        if self.player.rect.right > 1279:
            self.atMarket, self.inInventory, self.atBrew = False, False, False
            self.game.farmScreen.enter_state()
        
        if actions["e"]:
            if self.inInventory:
                self.inInventory = False
            else:
                self.inInventory = True
        if actions["w"]: 
            if self.atBrew:
                self.atBrew = False
            else:
                if self.player.rect.left < 165 and self.player.rect.top > 230 and self.player.rect.top < 390: #and self.player.rect.top < 100
                    self.atBrew = True
            if self.atMarket:
                self.atMarket = False
            else:
                if self.player.rect.left < 1000 and self.player.rect.right > 830 and self.player.rect.top < 170: #and self.player.rect.top < 100
                    self.atMarket = True  
        self.game.actions["w"] = False 
        self.game.actions["e"] = False
        self.game.actions["r"] = False
        if self.player.playerHealthStatus():
            self.game.gameOver()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.game.game_is_over = True

    def render(self, display):
        display.fill((211,211,211))
        pygame.display.set_caption("CITY OUTSKIRTS")
        display.blit(pygame.transform.scale(self.background, (1280, 720)), (0, 0))
        self.player.draw(display, self.img)
        
        self.npc1.draw()
        self.npc2.draw()
        self.npc3.draw()
        for x in range(len(self.npcs)):
            if self.npcs[x].moveable:
                self.npcs[x].npcMovement()
        self.npcOverlap(self.game.actions)
        self.player.displayHealth(self.game.screen)

        #INVENTORY
        if self.inInventory:
           self.player.showInventory(self.game.screen)
        #MARKET:
        if self.atMarket:
            self.showMarketScreen(self.game.screen, self.game.actions)
        #BREWERY
        if self.atBrew:
            self.showBrewScreen(self.game.screen, self.game.actions)
        #BREW QUEUE
        if self.currentlyBrewing:
            Shape.drawRect(Shape, display, 0, 0, 175, 55, (0, 0, 0))
            Shape.drawRect(Shape, display, 0, 0, 170, 50, (211, 211, 211))
            Shape.drawRect(Shape, display, 55, 0, 10, 50, (0, 0, 0))
            if len(self.timers) > 0:
                self.renderBrewQueue(display)

        if (pygame.time.get_ticks() - self.brewPopUP)/1000 <2 and self.brewPopUP != 0:
            self.popUp("Insufficient Materials!")
        if (pygame.time.get_ticks() - self.marketPopUP)/1000 <2 and self.marketPopUP != 0:
            self.popUp("Not Enough Gold!")
        
        if len(self.coins) >0:
            self.renderCoinsSpent(display)
        if len(self.ingredients) >0:
            self.renderBrewPlantsUsed()
        if len(self.questsCompleted) > 0:
            self.npcQuestCompleted()

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def showBrewScreen (self, screen, actions):
        Shape.drawRect(Shape, self.game.screen, 1280/2 - 400, 720/2 -250, 800, 600, (250,250,250))
        brew_img_surface = pygame.image.load("brew.xcf").convert_alpha()
        self.brewRect = pygame.rect.Rect(1280/2 -400, 720/2 -250, 800, 600)
        screen.blit(brew_img_surface, self.brewRect)

        locationCounter = -250
        for x in range(3): 
            text_surface = self.font.render(self.medicines1[x], True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (1280/2+ locationCounter +50, 720/2 + 150)

            screen.blit(text_surface, text_rect)
            locationCounter += 200

        screen.blit(pygame.image.load(self.medicines[0]), self.rect1)
        screen.blit(pygame.image.load(self.medicines[1]), self.rect2)
        screen.blit(pygame.image.load(self.medicines[2]), self.rect3)                
        counter = 0
        index = 0
        for key in self.recipeIngredientsDisplay:
            text_surface = self.font.render(key +":", True, (0,0,0))
            text_rect = text_surface.get_rect()
            xlocaiton = 1280/2 - 200 + counter
            text_rect.center =  (xlocaiton, 600)
            screen.blit(text_surface, text_rect)
            yincrement = 20
            for x in range(3):
                ingredient = self.font.render(self.recipeIngredientsDisplay[key][x] + " X " + str(self.recipeIngredientsAmounts[index][x]), True, (0,0,0,))
                ingredient_rect = ingredient.get_rect()
                ingredient_rect.center = (xlocaiton, 600+ 30 + yincrement )
                yincrement += 20
                screen.blit(ingredient, ingredient_rect)
            counter += 200
            index += 1
#FIXME: if inventory available, images change to color version image  
        #Event handling
        x, y = pygame.mouse.get_pos()
        if(abs(x - self.SCREEN_WIDTH/2 +200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[0] = True
        if(abs(x - self.SCREEN_WIDTH/2) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[1] = True
        if(abs(x - self.SCREEN_WIDTH/2 - 200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[2] = True

        for x in range(3):
            if self.itemSelected[x]:
                self.itemLocations[x].top = 720/2 -50
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player.checkMaterials(list(self.recipeIngredientsDisplay.values())[x], self.recipeIngredientsAmounts[x]):
                            self.currentlyBrewing = True
                            self.addToBrewQueue(x)
                            xx = self.itemLocations[x].x
                            yy = self.itemLocations[x].y
                            index = x
                            self.ingredients.append([xx, yy, pygame.time.get_ticks(), index])
                        else:
                            self.brewPopUP = pygame.time.get_ticks()                            
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            self.atBrew = False 
            else:
                self.itemLocations[x].top = 720/2
        #reset
        for x in range(3):
            self.itemSelected[x] = False

    def showMarketScreen(self, screen, actions):
        self.marketRect = pygame.rect.Rect(1280/2 -400, 720/2 -250, 800, 500)
        Shape.drawRect(Shape, self.game.screen, 1280/2 - 400, 720/2 -250, 800, 500, (250,250,250))
        market_img_surface = pygame.image.load("MARKET.xcf").convert_alpha()
        screen.blit(market_img_surface, self.marketRect)
        locationCounter = -250
        img_surface = pygame.image.load(self.coinimg).convert_alpha()
        transformed_img = pygame.transform.scale(img_surface, (50, 50))

        for x in range(3): 
            #prices
            text_surface = self.font.render("X " + str(self.itemPrices[x]), True, (0,0,0))
            img_rect = transformed_img.get_rect()
            text_rect = text_surface.get_rect()
            text_rect.center = (1280/2+ locationCounter +70, 720/2 + 125)
            img_rect.center = (1280/2 +locationCounter +30, 720/2 +125)
            
            screen.blit(transformed_img, img_rect)
            screen.blit(text_surface, text_rect)
            locationCounter += 200

        screen.blit(self.img_surface1, self.rect1)
        screen.blit(self.img_surface2, self.rect2)
        screen.blit(self.img_surface3, self.rect3)

        #Event handling
        x, y = pygame.mouse.get_pos()
        if(abs(x - self.SCREEN_WIDTH/2 +200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[0] = True
        if(abs(x - self.SCREEN_WIDTH/2) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[1] = True
        if(abs(x - self.SCREEN_WIDTH/2 - 200) <= 50 and abs(y- 410) <= 50):
            self.itemSelected[2] = True

        for x in range(3):
            if self.itemSelected[x]:
                self.itemLocations[x].top = 720/2 -50
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player.canPurchase(self.itemPrices[x]):
                            self.player.decreaseGold(self.itemPrices[x])
                            xx = self.itemLocations[x].left
                            y = self.itemLocations[x].top
                            self.coins.append([pygame.time.get_ticks(), self.itemPrices[x] * -1, [xx, y]])
                            self.player.addToInventory(self.marketListItems[x])
                        else:
                            self.marketPopUP = pygame.time.get_ticks()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            self.atMarket = False
            else:
                self.itemLocations[x].top = 720/2
        #reset
        for x in range(3):
            self.itemSelected[x] = False

    def addToBrewQueue(self, num):
        self.brewQueue.append(self.medicines[num])
        self.temps.append(self.medicines1[num])
        self.timers.append(pygame.time.get_ticks())

    def renderBrewQueue(self, screen):
        currentTime = math.floor((pygame.time.get_ticks() - self.timers[0])/1000)
        if currentTime < 5:
            text_surface1 = self.font.render(str(5 - currentTime), True, (0,0,0))
            text_surface2 = self.font.render("brewing..", True, (0,0,0))
            text_rect1 = text_surface1.get_rect()
            text_rect2 = text_surface2.get_rect()
            text_rect2.w, text_rect2.h = 100, 50
            text_rect2.center = (120, 40)
            temp = pygame.rect.Rect(0, 0, 70, 50)
            #Shape.drawRect(Shape, screen, 0, 120, 100, 175 - x, 10)
            Shape.drawRect(Shape, screen, 0, 50, 175, 15, (0, 0, 0))
            pygame.draw.rect(screen, (0,250,0), pygame.Rect(0,50,170*(currentTime/5),10))

            img_surface = pygame.transform.scale(pygame.image.load(self.brewQueue[0]).convert_alpha(), (50, 50))
            screen.blit(img_surface, temp)
            screen.blit(text_surface1, text_rect1)
            screen.blit(text_surface2, text_rect2)

        else:
            self.player.addToInventory(self.temps[0])
            self.temps.pop(0)
            self.brewQueue.pop(0)
            self.timers.pop(0)
            if len(self.timers) > 0:
                self.timers[0] = pygame.time.get_ticks()
            else:
                self.currentlyBrewing = False

    #implement escape button or whatevs to go back to title
    #we need some images for npc and enemies. gimp or internet


#FIXME add all the images that we need for brew screen, possible sword animation


    def npcOverlap(self, actions):
        for x in range(3):
            #if self.player.getRect().colliderect(self.npcRects[x]):
            if abs(self.npcRects[x].x - self.player.rect.x) <= 120 and abs(self.npcRects[x].y - self.player.rect.y) <= 120: 
                self.npcs[x].moveable = False
                #self.npcs[x].checkIfHasRequests()
                self.npcs[x].showRequest()
                if actions["t"] and self.player.checkMedicine(self.npcs[x].numOfMedicine, self.npcs[x].typeOfMedicine):
                    #self.npc.questIsCompleted()
                    print("eyuh")
                    temp = "medicine"
                    for y in range(len(self.medicines1)):
                        if self.npcs[x].typeOfMedicine == self.medicines1[y]:
                            temp = self.medicines[y]
                            break
                    self.questsCompleted.append([self.npcs[x].numOfMedicine, temp, pygame.time.get_ticks(), 1280/2, 720/2])
                    self.npcs[x].generateNpcRequests()
                    self.player.increaseGold(5)
            else:
                self.npcs[x].moveable = True 
                self.npcs[x].showBubbles(self.game.screen)
        #self.game.actions["t"] = False
    def popUp(self, msg):
        Shape.drawRect(Shape,self.game.screen, 1280/2 -125, 0, 250, 40, (175,175,175))
        text_surface = self.font.render(msg, True, (0,0,0))
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (100, 100))
        text_rect.topleft = (1280/2 - 115, 0)
        self.game.screen.blit(text_surface, text_rect)

    def renderFadingImage(self, x, y, screen, amount, img):
        text_surface = self.font.render(amount, True, (0,0,0))
        text_rect = text_surface.get_rect()
        pygame.transform.scale(text_surface, (50, 50))
        text_rect.topleft = (x, y)
        img_surface = pygame.image.load(img).convert_alpha()
        coin_rect = pygame.rect.Rect(x, y, 100, 100)
        screen.blit(pygame.transform.scale(img_surface, (50, 50)), coin_rect)
        screen.blit(text_surface, text_rect)



#        coin_img_surface = pygame.image.load(self.player.coinimg).convert_alpha()
 #       coin_rectangle = pygame.rect.Rect(rect.x, rect.y, 50, 50)
  #      display.blit(coin_img_surface, coin_rectangle)
   #     print("coin drop")
    #    pygame.time.delay(2000)

    def renderCoinsSpent(self, screen):
        for x in range(len(self.coins)):
            if (pygame.time.get_ticks() - self.coins[x][0])/1000 < 1:
                self.renderFadingImage(self.coins[x][2][0] + 20, self.coins[x][2][1] - 250, screen, "- " +str(self.coins[x][1]), self.coinimg)
                self.coins[x][2][1] -= 2
            else:
                self.coins.pop(x)
                break
    
    def npcQuestCompleted(self):
        for x in range(len(self.questsCompleted)):
            if (pygame.time.get_ticks() - self.questsCompleted[x][2])/1000 < 1:
                self.renderFadingImage(self.questsCompleted[x][3], self.questsCompleted[x][4], self.game.screen, "-"+ str(self.questsCompleted[x][0]), self.questsCompleted[x][1])
                self.renderFadingImage(self.questsCompleted[x][3], self.questsCompleted[x][4]+ 50, self.game.screen, "+10", self.coinimg)
                self.questsCompleted[x][4] -= 1
            else:
                self.questsCompleted.pop(x)
                break

    def renderBrewPlantsUsed(self):
        for x in range(len(self.ingredients)):
            if (pygame.time.get_ticks() - self.ingredients[x][2])/1000 < 1:
                #xx yy pypgame tick, index
                self.renderFadingImage(self.ingredients[x][0], self.ingredients[x][1], self.game.screen,"-" +str(self.recipeIngredientsAmounts[self.ingredients[x][3]][0]), self.recipeIngredientsImages[self.ingredients[x][3]][0])
                self.renderFadingImage(self.ingredients[x][0], self.ingredients[x][1] + 30, self.game.screen, "-" +str(self.recipeIngredientsAmounts[self.ingredients[x][3]][1]), self.recipeIngredientsImages[self.ingredients[x][3]][1])
                self.renderFadingImage(self.ingredients[x][0], self.ingredients[x][1]+ 60, self.game.screen, "-" +str(self.recipeIngredientsAmounts[self.ingredients[x][3]][2]), self.recipeIngredientsImages[self.ingredients[x][3]][2])
                self.ingredients[x][1] -= 2
                    
            else:
                self.ingredients.pop(x)
                break

#TODO test pop up for when completed request
#-- they dont take the medicine cant test pop up