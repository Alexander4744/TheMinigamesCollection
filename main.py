# Imports
import sys
import pygame
import snake
import spaceInv
import breakout

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))

font = pygame.font.Font('pixy.regular.ttf', 40)
titleFont = pygame.font.Font('pixy.regular.ttf', 60)

objects = []

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def mainMenu():

    customButton = Button(width/2 - 200, 3*90, 400, 80, 'Snake', lambda: snake.snakeGame(mainMenu, width, height, font))
    customButton = Button(width/2 - 200, 4*90, 400, 80, 'Space Invaders', lambda: spaceInv.spaceInvaders(mainMenu, width, height, font))
    customButton = Button(width/2 - 200, 5*90, 400, 80, 'Breakout', lambda: breakout.breakout(mainMenu, width, height, font))
    customButton = Button(width/2 - 200, 6*90, 400, 80, 'Quit', lambda: pygame.quit())
    screen.fill((0, 0, 0))

    # Game loop.
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object in objects:
            object.process()

        pygame.display.set_caption('Minigame Collection')
        pygame.display.flip()
        fpsClock.tick(fps)
        text = titleFont.render('Minigame Collection', False, (255, 255, 255))
        text_rect = text.get_rect(center=(width/2, 2*height/10))
        screen.blit(text, text_rect)
        pygame.display.update()

mainMenu()
