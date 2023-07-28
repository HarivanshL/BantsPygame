from state import State
from rect import Shape
from player import Player
from farmland import FarmScreen
import pygame

class Controls(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.background = pygame.image.load("title.xcf")
        self.font = pygame.font.SysFont(None, 30)
        self.BLACK = (0, 0, 0)
        self.possibleMoves = ["Q - Harvest Plant/Kill Enemy", "W - Open market/Show Brewing Station (in close proximity)", "E - Display Inventory", "R - Take Potion"]

    def render(self, display):
        display.fill((211,211,211))
        pygame.display.set_caption("CONTROLS")
        display.blit(pygame.transform.scale(self.background, (1280, 720)), (0, 0))
        self.backButton()
        mousePos = pygame.mouse.get_pos()
        Shape.drawCircle(Shape, self.game.screen, (211, 211, 211), mousePos, 10)
        Shape.drawRect(Shape, self.game.screen, 1280/2 -400, 720/2 -310, 800, 620, (175,175,175))
        increment = 150
        for x in range(len(self.possibleMoves)):
            text_surface = self.font.render(self.possibleMoves[x], True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (1280/2, increment)
            self.game.screen.blit(text_surface, text_rect)
            increment += 100


    def update(self, actions):
        if actions["back"]:
            self.game.state_stack.pop()
            pygame.time.delay(100)     
      

    def backButton(self):
        Shape.drawRect(Shape, self.game.screen, 0, 0, 200, 100, (175,175,175))
        text_surface = self.font.render("BACK", True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (100, 50)
        self.game.screen.blit(text_surface, text_rect)

