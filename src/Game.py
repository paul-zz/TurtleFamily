import pygame
from src.AssetsLoader import AssetsLoader
from src.LocaleManager import LocaleManager
import src.States


class Game:

    def __init__(self):
        self.state = None
        self.nextState = None
        self.highscore = 0

    def setHighScore(self, highscore : int):
        self.highscore = highscore

    def getHighScore(self):
        return self.highscore

    def run(self):
        # pygame initialization
        pygame.init()

        # display initiation
        screen_size = (1024,768)
        screen = pygame.display.set_mode(screen_size)

        pygame.mouse.set_visible(1)
        pygame.display.set_caption('Turtle Family')

        # Load Assets and Locale
        AssetsLoader.loadAllFromList("./assets/assetslist.yaml")
        LocaleManager.loadAllFromList("./assets/locale.yaml")
        LocaleManager.setFallback(3) # Set en-us as fallback
        
        #sound initiation
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load("./assets/sounds/bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        #FPS initiation
        clock = pygame.time.Clock() 
        rate = 60

        # Next state 
        self.nextState = src.States.Homepage(screen)
        #Main loop
        while 1:
            if self.state != self.nextState:
                self.state = self.nextState
                self.state.firstDisplay(screen)
            for event in pygame.event.get():
                self.state.handle(event)
            self.state.update(self)
            clock.tick(rate)