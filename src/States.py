import sys
import pygame

from .Turtle import Turtle
from .Ground import Ground

class State:
    def handle(self,event):
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

    def firstDisplay(self, screen, assets):
        pass
        # screen.blit(bg,(0,0))
        # pygame.display.flip()

    def display(self,screen):
        pass

class Paused(State):
    finished = 0
    image = None
    text = ''

    def handle(self, event):
        State.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            self.finished = 1

    def update(self, game):
        pass


class Level(State):
    def __init__(self, screen, assets):
        pygame.mixer.music.unpause()
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.assets = assets
        self.firstTurtle = Turtle(self.assets.getImage("turtle"), self.screen)
        self.turtlelst = []
        self.turtlelst.append(self.firstTurtle)
        self.sprites = pygame.sprite.RenderUpdates()
        self.ground = Ground(self.assets.getImage("ground"), self.screen_size[0], 50, self.screen_size[1] - 50)
        self.sprites.add(self.firstTurtle)
        self.sprites.add(self.ground)
        self.score = 0
        self.layer = 0

        self.bg = assets.getImage("background")
        self.turtle_img = assets.getImage("turtle")
        self.touchsound = assets.getSound("touch")
        self.niceshot_1 = assets.getSound("niceshot_1")
        self.niceshot_2 = assets.getSound("niceshot_2")

        self.score_font = self.assets.getFont("score_font")
        self.font1 = assets.getFont("bigfont")
        self.midfont = assets.getFont("midfont")

        self.show_score_addition = False
        self.time_end = 0

    def handle(self,event):
        if event.type== pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.touchsound.play()
            self.turtlelst[-1].drop_flag = True

    def update(self, game):
        self.sprites.update()
        score_text = self.score_font.render("得分:" + str(self.score), True, (0,0,0))
        highscore_text = self.score_font.render("最高分:" + str(game.getHighScore()), True, (0,0,0))
        self.screen.blit(score_text,(5,5))
        self.screen.blit(highscore_text,(self.screen_size[0]-100,5))
        pygame.display.update()
        
        if self.firstTurtle.collide(self.ground) and not self.firstTurtle.frozen:
            self.firstTurtle.freeze()
            self.firstTurtle.placeAfterCollide(self.ground)
            self.turtlelst.append(Turtle(self.turtle_img, self.screen))
            self.sprites.add(self.turtlelst[-1])
            self.score += 1
            self.layer += 1
            self.show_score_addition = True
            self.time_end = pygame.time.get_ticks() + 500

        if self.turtlelst[-1] != self.firstTurtle:
            if self.turtlelst[-1].collide(self.turtlelst[-2]) and not self.turtlelst[-1].frozen:
                self.turtlelst[-1].freeze()
                self.turtlelst[-1].placeAfterCollide(self.turtlelst[-2])
                if self.turtlelst[-1].rect.width > self.turtlelst[-2].rect.width: 
                    # GAME OVER
                    nextstate = GameOver(self.score, game, self.screen, self.assets)
                    game.nextState = nextstate
                else: 
                    # CONTINUE
                    self.score += self.layer
                    self.show_score_addition = True
                    self.time_end = pygame.time.get_ticks() + 500
                    eps = (self.turtlelst[-2].rect.width - self.turtlelst[-1].rect.width)/self.turtlelst[-2].rect.width # error of the width between two turtles
                    if eps<0.1:
                        text=self.font1.render("太厉害了",True,(0,0,0))
                        sound = self.niceshot_2
                        bonus = 5
                        if eps<0.05:
                            text=self.font1.render("真是神准",True,(0,0,0))
                            sound = self.niceshot_1
                            bonus = 10
                        self.score += bonus
                        text_bonus = self.midfont.render(f"奖励{bonus}分！", True, (0,0,0))
                        sound.play()
                        # Get bounds to make the text centered
                        center,top = self.screen.get_rect().center
                        height = self.font1.get_linesize()
                        r = text.get_rect()
                        r.midtop = center, top-height
                        # Get bounds to make the text centered
                        r2 = text_bonus.get_rect()
                        r2.midtop = center, r.top + r.height + 10
                        #sprites.clear(screen,clear_callback)
                        self.screen.blit(self.bg,(0,0))#screen.fill(bg)
                        self.sprites.update()
                        updates = self.sprites.draw(self.screen)
                        self.screen.blit(text,r)
                        self.screen.blit(text_bonus,r2)
                        self.screen.blit(score_text,(5,5))
                        self.screen.blit(highscore_text,(self.screen_size[0]-100,5))
                        pygame.display.update()
                        pygame.time.delay(1000)
                        self.screen.blit(self.bg,(0,0))#screen.fill(bg)
                        updates = self.sprites.draw(self.screen)
                        pygame.display.update(updates)
                        pygame.display.update()
                    self.layer += 1
                    self.turtlelst.append(Turtle(self.turtle_img, self.screen))
                    self.sprites.add(self.turtlelst[-1])
        
        if self.show_score_addition:
            if pygame.time.get_ticks() < self.time_end:
                text = self.score_font.render("+ " + str(self.layer), True, (0,0,0))
                self.screen.blit(text, (5, 30))
                pygame.display.update()
            else:
                self.show_score_addition = False
    
    def display(self, screen):
        screen.blit(self.bg,(0,0))#screen.fill(bg)
        updates = self.sprites.draw(screen)
        pygame.display.update(updates)
        

class Instruction(Paused):

    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.center, self.top = screen.get_rect().center

    def firstDisplay(self, screen, assets):
        # Load assets
        self.bg = assets.getImage("background")
        self.sound_letsplay = assets.getSound("letsplay")
        self.sound_ready = assets.getSound("ready")
        self.font = assets.getFont("instruction_font")
        # Init display
        
        self.displayInstructionWithAudio(screen, self.bg, "不可以比下面的乌龟大哦", self.font, self.sound_letsplay, 1000, (0, 0, 0))
        self.displayInstructionWithAudio(screen, self.bg, "Ready?", self.font, self.sound_ready, 500, (255, 0, 0))
        self.displayInstructionWithAudio(screen, self.bg, "GO!", self.font, None, 500, (255, 0, 0))
        self.finished = 1


    def displayInstructionWithAudio(self, screen, bg, text, font, audio, delay = 500, color = (0, 0, 0)):
        # Fill the screen with bg color
        screen.blit(bg,(0, 0))
        # Render the line
        line = font.render(text, 1, color)
        height = self.font.get_linesize()
        # Get the bounding rectangle of the text and make it centered
        r = line.get_rect()
        r.midtop = self.center, self.top-height/2
        screen.blit(line, r)
        pygame.display.flip()
        # Play the audio if it exists
        if audio:
            audio.play()
        # Delay time to display the instruction page
        pygame.time.delay(delay)
    
    def update(self, game):
        if self.finished:
            game.nextState = Level(self.screen, self.assets)


class GameOver(Paused):

    def __init__(self, score, game, screen, assets):
        self.score = score
        self.game = game
        self.screen = screen
        self.assets = assets

        self.sound_fail = assets.getSound("fail")
        self.sound_newbest = assets.getSound("newbest")

    def firstDisplay(self, screen, assets):
        # Update the highscore
        highscore = self.game.getHighScore()
        if self.score <= highscore or highscore==0:
            if highscore ==0:
                self.game.setHighScore(self.score)
            pygame.mixer.music.pause()
            self.sound_fail.play()
            font = assets.getFont("bigfont")
            height = font.get_linesize()
            center,top = screen.get_rect().center
            top -= height//2
            line = font.render('太可惜了',1,(255,0,0))
            r = line.get_rect()
            r.midtop = center,top
        else:
            self.game.setHighScore(self.score)
            self.sound_newbest.play()
            font = font = assets.getFont("bigfont")
            height = font.get_linesize()
            center,top = screen.get_rect().center
            top -= height//2
            line = font.render('新的记录！',1,(255,0,0))
            r = line.get_rect()
            r.midtop = center,top
        font = assets.getFont("midfont")
        text = font.render('得分：' + str(self.score), 1, (255,255,255))
        top = r.top + r.height + 10
        center = r.center[0]
        r2 = text.get_rect()
        r2.midtop = center,top
        screen.blit(line, r)
        screen.blit(text, r2)
        pygame.display.flip()

    def update(self, game):
        if self.finished:
            game.nextState = Level(self.screen, self.assets)


class Homepage(Paused):
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

    def firstDisplay(self, screen, assets):
        self.bg = assets.getImage("background")
        self.font = assets.getFont("bigfont")
        screen.blit(self.bg, (0, 0))
        height = self.font.get_linesize()
        center, top = screen.get_rect().center
        top -= height // 2
        line = self.font.render('乌龟家族', 1, (0, 0, 0))
        r = line.get_rect()
        r.midtop = center, top
        screen.blit(line, r)
        pygame.display.flip()

    def update(self, game):
        if self.finished:
            game.nextState = Instruction(self.screen, self.assets)