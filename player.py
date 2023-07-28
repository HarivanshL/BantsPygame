import pygame
from rect import Shape

class Player:
    def __init__(self, game):
        self.game = game
        self.x = 50
        self.y = 250
        player_w, player_h = 100, 100
        self.rect = pygame.rect.Rect(30, 30, player_w, player_h)
        self.images = ["Honey.xcf", "Potion.xcf", "medicine3.xcf", "Lavender.xcf", "ROSE.xcf", "MINT.xcf", "medicine1.xcf", "medicine2.xcf", "ointment.xcf"]
        self.inventory = {"Honey": 0, "Potion": 0, "Vinegar": 0, "Lavender": 0, "Rose": 0, "Mint": 0, "Penecillin": 0, "Electuary": 0, "Ointment": 0}
        self.itemNames = ["Honey", "Potion", "Vinegar", "Lavender", "Rose", "Mint", "Penecillin", "Electuary", "Ointment"]
        self.inventoryAmounts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.img = "BACKGROUND_CITY.xcf"
        self.coinimg = "COIN.xcf"
        self.health = 100
        self.gold = 40
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0,0,0)
        self.turned = False
        self.font = pygame.font.SysFont(None, 30)
        self.hitting = False
        self.talkingToNpc = False
        self.healthDecreasing = False
        self.moveable = True
        self.isDead = False
        self.canMove = True
        self.moveLast = 0
        self.lastTimePoisoned = 0

    def getRect(self):
        return self.rect

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def draw(self, screen, img):    
        if self.game.actions["q"]:
            self.hitting = True
        if self.turned:
            if self.hitting:
                img_surface = pygame.image.load("doctor_hitting_turned.xcf").convert_alpha()
            elif not self.hitting:
                img_surface = pygame.image.load("doctor2.xcf").convert_alpha()
        else:
            if self.hitting:
                img_surface = pygame.image.load("doctor_hitting.xcf").convert_alpha()
            elif not self.hitting:
                img_surface = pygame.image.load(img).convert_alpha()
        screen.blit(img_surface, self.rect)
        self.hitting =False

    def resetLocation(self, x, value):
        if value:
            self.rect.left = x
        else:
            self.rect.right = x

    def moveFarm(self, key, screen_w, screen_h):   
        if key[pygame.K_UP]:
            self.rect.move_ip(0, -2)
        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, 2)
        if key[pygame.K_LEFT]:
            self.turned = False
            self.rect.move_ip(-2, 0)        
        if key[pygame.K_RIGHT]:
            self.turned = True   
            self.rect.move_ip(2, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h     

    def moveMain(self, key, screen_w, screen_h, xlocations, npcs):
        for x in range(len(npcs)):
            if npcs[x].rect.colliderect(self.rect):            
                x_val = npcs[x].rect.x - self.rect.x
                y_val = npcs[x].rect.y - self.rect.y

        if self.canMove:
            if key[pygame.K_UP]:
                if not(self.rect.top < 105 and self.rect.right > 680 and self.rect.left < 1140):
                    self.rect.move_ip(0, -2)
                    self.moveLast = (0, 2)
            if key[pygame.K_DOWN]:
                self.rect.move_ip(0, 2)
                self.moveLast = (0, -2)
            if key[pygame.K_LEFT]:
                self.turned = False
                if not(self.rect.top <=100 and (self.rect.right > 670 and self.rect.left < 1155)):
                    self.rect.move_ip(-2, 0)
                    self.moveLast = (2, 0)
                else:
                    if self.rect.left - 1155 > -5:
                        self.rect.left = 1160     
    
            if key[pygame.K_RIGHT]:
                self.turned = True 
                if not(self.rect.top <=100 and (self.rect.right > 670 and self.rect.left < 1155)):
                    self.rect.move_ip(2, 0)
                    self.movelast = (-2, 0)
                else:
                    if 670 - self.rect.right < -5:
                        self.rect.left = 1155 
    
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_w:
                self.rect.right = screen_w
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screen_h:
                self.rect.bottom = screen_h   

    def showInventory(self, screen):
        inventory_img_surface = pygame.image.load("pack.xcf").convert_alpha()
        self.inventoryRect = pygame.rect.Rect(0, 720/4, 370, 280)
        screen.blit(inventory_img_surface, self.inventoryRect)

        offsetx = 0
        offsety = 0

        for x in range(9):
            #reset
            if x % 3 == 0 and x != 0:
                offsetx = 0
                offsety += 90
            img_surface = pygame.image.load(self.images[x]).convert_alpha()
            transformed_img = pygame.transform.scale(img_surface, (50, 50))
            text_surface = self.font.render("X " + str(self.inventoryAmounts[x]), True, (0,0,0))
            transformed_txt = pygame.transform.scale(text_surface, (20, 20))
            img_rect = transformed_img.get_rect()
            text_rect = transformed_txt.get_rect()
            text_rect.topleft = (offsetx + 70, 720/4 + offsety+25)
            img_rect.topleft = (offsetx, 720/4 + offsety)
            
            screen.blit(transformed_img, img_rect)
            screen.blit(transformed_txt, text_rect)
            offsetx+=90
        #Health bar:
        Shape.drawRect(Shape, screen, 720-100, 1280 - 100, 100, 100, (175,175,175))
        img_surface = pygame.image.load(self.coinimg).convert_alpha()
        screen.blit(img_surface, (1280-100, 720-100))
        text_surface = self.font.render(str(self.gold), True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (1280-120, 670)
        screen.blit(text_surface, text_rect)
    


    def displayHealth(self, screen):
        #FIXME:
        black_rect = pygame.rect.Rect(self.rect.x -10, self.rect.y -10, 10, 50)
        pygame.draw.rect(screen, (0, 0, 0), black_rect)
        rect = pygame.rect.Rect(self.rect.x, self.rect.y , 10, self.health/2)
        rect.bottomleft = black_rect.bottomleft

        if self.health > 60:
            pygame.draw.rect(screen, (0, 250, 0), rect)
        elif self.health >20:
            pygame.draw.rect(screen, (255, 219, 88), rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), rect)

    def addToInventory(self, item):
        for x in range(9):
            if self.itemNames[x] == item:
                self.inventory[item] = self.inventory[item] +1
                self.inventoryAmounts[list(self.inventory.keys()).index(item)] += 1

    def harvestPlant(self, cropLocations, types, cropTypes, size):
        for o in range(len(cropLocations)):
            if abs(self.rect.top - cropLocations[o][1]) <=100 and abs(self.rect.left - cropLocations[o][0]) <=100:
                cropLocations.pop(o)                
                self.inventory[cropTypes[types[o]]] += 1
                types.pop(o)
                size -= 1

    def loseHealth(self):
        self.health = self.health-5
        if self.health <= 0:
            self.isDead = True
            return True
        else:
            return False

    def playerHealthStatus(self):
        if self.healthDecreasing:
            time = pygame.time.get_ticks() - self.lastTimePoisoned
            print(time)
            if (time) % 1000 < 5:
                #FIXME: only lose health bar every 10 seconds, for 50 seconds
                return self.loseHealth()
            if (time)/1000 >= 15:
                self.healthDecreasing = False

    def addHealth(self):
        self.healthDecreasing = False
        self.health += 20   
        if self.health > 100:
            self.health = 100

    def decreaseGold(self, amount):
        self.gold -= amount
    
    def increaseGold(self, amount):
        self.gold += amount

    #enemy class is abstract; rats bear
    #shopkeeper; put image transaparent; set items with images; set "are you sure" box
    #plague docta; collect ingredients/ medicine
    #go to table; turn in ingredients>medicine
    #background changes
    #timer and progress bar for plant growth
    #random timed voicelines
    #medicine on self or npc

    def moveWithCollides(self, key, screen_w, screen_h, rect):    
        if key[pygame.K_UP]:
            self.rect.move_ip(0, -2)
            if self.rect.colliderect(rect):
                self.rect.top = rect.bottom
                self.rect.move_ip(0, 2)
        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, 2)
            if self.rect.colliderect(rect):
                self.rect.bottom = rect.top
        if key[pygame.K_LEFT]:
            self.rect.move_ip(-2, 0)  
            self.turned = False
            if self.rect.colliderect(rect):
                self.rect.left = rect.right 
        if key[pygame.K_RIGHT]:
            self.turned = True
            self.rect.move_ip(2, 0)
            if self.rect.colliderect(rect):
                self.rect.right = rect.left 
   
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h 

    def checkMaterials(self, ingredients, ingredient_amounts):
        if self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[0])] >= ingredient_amounts[0] and self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[1])] >= ingredient_amounts[1] and self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[2])] >= ingredient_amounts[2]:
            self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[0])] -= ingredient_amounts[0]
            self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[1])] -= ingredient_amounts[1]
            self.inventoryAmounts[list(self.inventory.keys()).index(ingredients[2])] -= ingredient_amounts[2]
            return True
        return False
        
    def checkMedicine(self, num, type):
        if self.inventoryAmounts[list(self.inventory.keys()).index(type)] >= num:
            self.inventoryAmounts[list(self.inventory.keys()).index(type)] -= num
            return True
        else:
            return False
        
    def checkPotion(self):
        if self.inventoryAmounts[list(self.inventory.keys()).index("Potion")] > 0:
            return True
        else:
            return False
        
    def canPurchase(self, amount):
        if self.gold - amount >= 0:
            return True
        else:
            return False
