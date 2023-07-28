import pygame

from rect import Shape
from farm import Farm
from mainscreen import Main
from title import Title
from farmland import FarmScreen                                     
from credits import Credits
from controls import Controls

class Real():
    def __init__(self):
            pygame.init()
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 1280, 720
            self.GAME_W,self.GAME_H = 480, 270
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
            self.mainScreen = Main(self)
            self.farmScreen = FarmScreen(self)
            self.creditsScreen = Credits(self)
            self.controlsScreen = Controls(self)
           
            self.running, self.playing = True, True
            self.actions = {"e": False, "back": False, "escape": False, "w": False, "quit": False, "tab": False,"credits": False, "started": False, "left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False, "q" : False, "controls" : False, "r" : False, "t": False}
            self.state_stack = []   
            self.background = pygame.image.load("BACKGROUND.xcf")
            self.plagueDoctor = pygame.image.load("doctor.xcf")
            self.lastTimeGameIsOver = 0
            self.game_is_over = False
            self.font = pygame.font.SysFont(None, 30)

            

    def get_events(self):
        x, y = pygame.mouse.get_pos()            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 360) <= 45):
                    #if (x >= 490 and x <= 790) and (y >= 320 and y <= 410):
                    self.actions["quit"] = True
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 240) <= 45):
                    #if (x >= 490 and x <= 790) and (y >= 240 and y <= 410):
                    self.actions['started'] = True 
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 480) <= 45):
                    self.actions['credits'] = True
                if(abs(x - 100) <= 100 and abs(y- 50) <= 50):
                    self.actions['back'] = True  
                if(abs(x - self.SCREEN_WIDTH/2) <= 150 and abs(y- 600) <= 45):
                    self.actions['controls'] = True   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = True
                    #self.playing = False
                    #self.running = False
                #if event.key == pygame.K_TAB:
                #    self.actions['tab'] = True
                if event.key == pygame.K_a:
                    self.actions['left'] = True
               # if event.key == pygame.K_r:
                #    self.actions['r'] = True
                if event.key == pygame.K_q:
                    self.actions["q"] = True
                if event.key == pygame.K_t:
                    self.actions["t"] = True
                    #self.farmScreen.harvest(x, y)
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                #if event.key == pygame.K_w:
                #    self.actions['w'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True    
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True  
            if event.type == pygame.MOUSEBUTTONUP:
                self.actions["quit"] = False
                self.actions['started'] = False
                self.actions['credits'] = False
                self.actions['back'] = False
                self.actions['controls'] = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    self.actions['e'] = True
                if event.key == pygame.K_r:
                    self.actions['r'] = True
                if event.key == pygame.K_t:
                    self.actions['t'] = False
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_q:
                    self.actions["q"] = False   
                if event.key == pygame.K_w:
                    self.actions["w"]  = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False  

            #if pygame.mouse.get_pressed()[0] and mouse

    def update(self):
        self.state_stack[-1].update(self.actions)

    def render(self):
        self.state_stack[-1].render(self.screen)
        # Render current state to the screen
        #self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def gameOver(self):
        self.lastTimeGameIsOver = pygame.time.get_ticks()
        Shape.drawRect(Shape, self.screen, 1280/2 -400, 720/2 -310, 800, 620, (175,175,175))
        #if self.player.isDead:
        #    text_surface = self.font.render("GAME OVER!!! LOSER... You DIED", True, (0,0,0))
        #else:
        text_surface = self.font.render("GAME OVER! You KILLED the villagers!!!", True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (1280/2 -400, 720/2 -310)
        self.screen.blit(text_surface, text_rect)

    def game_loop(self):
        while self.playing:
            #self.get_dt()
            self.get_events()
            self.update()
            self.render()
            self.farmScreen.runFarm()
            if self.game_is_over:
                self.state_stack.clear()
                self.state_stack.append(t)
                self.mainScreen = Main(self)
                self.farmScreen = FarmScreen(self)
                self.game_is_over = False


#game = Game()
#game.__init__()
#game.main_loop()

g = Real()
t = Title(g)
c = Credits(g)
g.state_stack.append(t)
while g.running:
    g.game_loop()

#timer pass as argument
#Have reset function in farm screen reset per a certain condition
#Have reset function rest crop locations and amounts and despawn based on timer
#Have rats spawn separately from crops 

#FIXME going back and forth in the credits and controls messes it up
#issue is you just gotta move the game logic for each state in the update part as opposed to leaving it in game get events

#TODO
#VISUALS:
#Rats "drop" coins animation
#+1 animation when gaining items 
#Visuals on title and credits/controls

#INVENTORY:
#visuals on inventory 
#glitcy inventory
#inventory and walking fix on farm/main

#MISC:
#background on brew
#Rats need to take away health
#timers on everything to make game harder/easier

#FIXME fucked variable names (ie rectum, numeros), farmland
#FIXME fix to where you can visit credits or controls on click
#FIXME implement game clock so that way farm screen still spawns /mayhaps very difficult
#FIXME implement game over to reset the pygame last ticks for npc requests