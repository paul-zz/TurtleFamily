import pygame
import src.States
import src.AssetsLoader

class Game:
    def __init__(self):
        self.state = None
        self.nextState = src.States.Homepage()
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

        # Assets Initialization
        assets = src.AssetsLoader.AssetsLoader()
        assets.loadAllFromList("./assets/assetslist.yaml")

        bg = assets.getImage("background")
        bg = bg.convert()
        bg = pygame.transform.scale(bg,(screen_size[0],screen_size[1]))
        pygame.mouse.set_visible(1)
        pygame.display.set_caption('Turtle Family')
        

        #sound initiation
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load("./assets/sounds/bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        #FPS initiation
        pygame.time.Clock().tick(60)

        #highscore initiation
        # TODO : highscore implementation without using global variables

        #Main loop
        while True:
            if self.state != self.nextState:
                self.state = self.nextState
                self.state.firstDisplay(screen, assets)
            for event in pygame.event.get():
                self.state.handle(event)
            self.state.update(self, screen, assets)
            self.state.display(screen)