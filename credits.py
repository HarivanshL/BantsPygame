from state import State
from rect import Shape
from player import Player
from farmland import FarmScreen
import pygame

class Credits(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.width, self.height = game.SCREEN_WIDTH, game.SCREEN_HEIGHT
        self.game = game
        self.background = pygame.image.load("title.xcf")
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)
        self.buttonLocations = [[self.height/2 - self.height/6, 300, 240], [self.height/2 + self.height/6, 300, 480]]
        self.buttonHeight = 90
        self.creditsMessages = ["We hope you enjoyed our first game,", "Thank you for playing!!", "Created by: Brianna Patten and Harivansh Luchmun"]
        self.buttonLabels = ["PATTEN AND HARBAN", "BACK" ]

    def render(self, display):
        display.fill((211,211,211))
        pygame.display.set_caption("CREDITS")
        display.blit(pygame.transform.scale(self.background, (1280, 720)), (0, 0))
        #self.drawButtons(display)
        mousePos = pygame.mouse.get_pos()
        Shape.drawCircle(Shape, self.game.screen, (211, 211, 211), mousePos, 10)
        self.backButton()
        Shape.drawRect(Shape, self.game.screen, 1280/2 -400, 720/2 -310, 800, 620, (175,175,175))
        increment = 150
        for x in range(len(self.creditsMessages)):
            text_surface = self.font.render(self.creditsMessages[x], True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (1280/2, increment)
            self.game.screen.blit(text_surface, text_rect)
            increment += 100
        
    def update(self, actions):
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if(abs(x - self.width/2) <= 300/2 and abs(y- self.buttonLocations[0][0]) <= 90/2):
                if(abs(x - self.width/2) <= 150 and abs(y- self.buttonLocations[1][2]) <= 45):
                    print("POP")
                    self.game.exit_state()
                    pygame.time.delay(100)
                #if(abs(x - self.width/2) <= 300/2 and abs(y- self.buttonLocations[0][1]) <= 90/2):
        if actions["back"]:
            self.game.state_stack.pop()
            pygame.time.delay(100)     
        

    def drawButtons(self, screen):
        for x in range(len(self.buttonLocations)):
            Shape.drawRect(Shape, screen, self.width/2 - self.buttonLocations[x][1]/2, self.buttonLocations[x][2] - 90/2, self.buttonLocations[x][1], self.buttonHeight, (175,175,175))
            text_surface = self.font.render(self.buttonLabels[x], True, self.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (self.width/2, self.buttonLocations[x][0])
            screen.blit(text_surface, text_rect)

    def backButton(self):
        Shape.drawRect(Shape, self.game.screen, 0, 0, 200, 100, (175,175,175))
        text_surface = self.font.render("BACK", True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (100, 50)
        self.game.screen.blit(text_surface, text_rect)
