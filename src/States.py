import sys
import pygame
import webbrowser

from pygame.math import Vector2

from .Turtle import Turtle
from .Ground import Ground
from .Camera import Camera
from .AssetsLoader import AssetsLoader
from .LocaleManager import LocaleManager
from .OptionBox import OptionBox
from .PushButton import PushButton
from .SwitchButton import SwitchButton
from .LabelBox import LabelBox
from .Gauge import Gauge

class State:
    def handle(self,event):
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

    def firstDisplay(self, screen : pygame.Surface):
        pass
        # screen.blit(bg,(0,0))
        # pygame.display.flip()


class Paused(State):
    finished = 0
    
    def handle(self, event):
        State.handle(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            self.finished = 1

    def update(self, game):
        pass


class Level(State):
    def __init__(self, screen : pygame.Surface):
        pygame.mixer.music.unpause()
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.firstTurtle = Turtle(self.screen)
        self.turtlelst = []
        self.turtlelst.append(self.firstTurtle)
        self.sprites = pygame.sprite.RenderUpdates()
        self.ground = Ground(self.screen_size[0], 50, self.screen_size[1] - 50)
        self.sprites.add(self.firstTurtle)
        self.sprites.add(self.ground)
        self.score = 0
        self.layer = 0

        self.bg = AssetsLoader.getImage("background")
        self.turtle_img = AssetsLoader.getImage("turtle")
        self.touchsound = AssetsLoader.getSound("touch")
        self.niceshot_1 = AssetsLoader.getSound("niceshot_1")
        self.niceshot_2 = AssetsLoader.getSound("niceshot_2")

        self.score_font = AssetsLoader.getFont("score_font")
        self.font1 = AssetsLoader.getFont("bigfont")
        self.midfont = AssetsLoader.getFont("midfont")

        self.start_camera_follow = False
        self.camera = Camera(Vector2(self.screen_size[0]/2, self.screen_size[1]/2))
        self.camera.addSprite(self.firstTurtle)
        self.camera.addSprite(self.ground)

        self.show_score_addition = False
        self.time_end = 0

        self.back_to_home = False

    def handle(self,event):
        if event.type== pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.back_to_home = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.touchsound.play()
            self.turtlelst[-1].drop_flag = True

    def update(self, game):
        # Update all sprites
        if self.back_to_home:
            game.nextState = Homepage(self.screen)

        self.sprites.update()
        
        if self.firstTurtle.collide(self.ground) and not self.firstTurtle.frozen:
            self.firstTurtle.freeze()
            self.firstTurtle.placeAfterCollide(self.ground)
            self.turtlelst.append(Turtle(self.screen))
            self.sprites.add(self.turtlelst[-1])
            self.camera.addSprite(self.turtlelst[-1])
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
                    nextstate = GameOver(self.score, game, self.screen)
                    game.nextState = nextstate
                else: 
                    # CONTINUE
                    self.score += self.layer
                    self.show_score_addition = True
                    self.time_end = pygame.time.get_ticks() + 500
                    eps = (self.turtlelst[-2].rect.width - self.turtlelst[-1].rect.width)/self.turtlelst[-2].rect.width # error of the width between two turtles
                    if eps<0.1:
                        bonus_banner_str = LocaleManager.getString("niceshot_2")
                        bonus_sound = self.niceshot_2
                        bonus = 5
                        if eps<0.05:
                            bonus_banner_str = LocaleManager.getString("niceshot_1")
                            bonus_sound = self.niceshot_1
                            bonus = 10
                        self.score += bonus
                        # Play bonus sound
                        bonus_sound.play()

                        # Render bonus text
                        text_bonus_banner = self.font1.render(bonus_banner_str,True,(0,0,0))
                        text_bonus = self.midfont.render(LocaleManager.getString("bonus")%bonus, True, (0,0,0))

                        # Get bounds to make the text centered
                        center,top = self.screen.get_rect().center
                        height = self.font1.get_linesize()
                        r = text_bonus_banner.get_rect()
                        r.midtop = center, top-height
                        # Get bounds to make the text centered
                        r2 = text_bonus.get_rect()
                        r2.midtop = center, r.top + r.height + 10

                        self.screen.blit(self.bg,(0,0))
                        self.sprites.update()
                        updates = self.sprites.draw(self.screen)
                        updates.append(self.screen.blit(text_bonus_banner,r))
                        updates.append(self.screen.blit(text_bonus,r2))
                        pygame.display.update(updates)
                        pygame.time.delay(1000)
                    self.layer += 1
                    self.turtlelst.append(Turtle(self.screen))
                    self.sprites.add(self.turtlelst[-1])
                    self.camera.addSprite(self.turtlelst[-1])
        
        if self.show_score_addition:
            if pygame.time.get_ticks() < self.time_end:
                text_score_addition = self.score_font.render("+ " + str(self.layer), True, (0,0,0))
                text_score_addition_update = self.screen.blit(text_score_addition, (5, 30))
                pygame.display.update(text_score_addition_update)
            else:
                self.show_score_addition = False
        
        # Update Camera follow
        if self.turtlelst[-1] != self.firstTurtle and self.turtlelst[-2].getPos().y < self.screen_size[1]/2:
            # Start camera follow
            self.camera.follow(self.turtlelst[-2])
            
        self.camera.updatePosition()

        # Draw indicator
        score_text = self.score_font.render(LocaleManager.getString("score") + str(self.score), True, (0,0,0))
        highscore_text = self.score_font.render(LocaleManager.getString("highscore") + str(game.getHighScore()), True, (0,0,0))
        
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(score_text,(5,5))
        self.screen.blit(highscore_text,(self.screen_size[0]-highscore_text.get_rect().width-5,5))

        # Update display of the frame
        self.sprites.draw(self.screen)
        pygame.display.update()
    
        

class Instruction(Paused):

    def __init__(self, screen : pygame.Surface):
        self.screen = screen
        self.center, self.top = screen.get_rect().center

    def firstDisplay(self, screen : pygame.Surface):
        # Load assets
        self.bg = AssetsLoader.getImage("background")
        self.sound_letsplay = AssetsLoader.getSound("letsplay")
        self.sound_ready = AssetsLoader.getSound("ready")
        self.font = AssetsLoader.getFont("instruction_font")
        # Init display
        
        self.displayInstructionWithAudio(screen, self.bg, LocaleManager.getString("instruction_1"), self.font, self.sound_letsplay, 1000, (0, 0, 0))
        self.displayInstructionWithAudio(screen, self.bg, LocaleManager.getString("ready"), self.font, self.sound_ready, 500, (255, 0, 0))
        self.displayInstructionWithAudio(screen, self.bg, LocaleManager.getString("go"), self.font, None, 500, (255, 0, 0))
        self.finished = 1


    def displayInstructionWithAudio(self, 
                                    screen : pygame.Surface, 
                                    bg : pygame.Surface, 
                                    text : str, 
                                    font : pygame.font.Font, 
                                    audio : pygame.mixer.Sound, 
                                    delay : int = 500, 
                                    color : tuple[int, int, int] = (0, 0, 0)):
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
            game.nextState = Level(self.screen)


class GameOver(Paused):

    def __init__(self, score : int, game, screen : pygame.Surface):
        self.score = score
        self.game = game
        self.screen = screen

        self.sound_fail = AssetsLoader.getSound("fail")
        self.sound_newbest = AssetsLoader.getSound("newbest")

        self.return_to_home = False

    def firstDisplay(self, screen : pygame.Surface):
        # Update the highscore
        highscore = self.game.getHighScore()
        if self.score <= highscore or highscore==0:
            if highscore ==0:
                self.game.setHighScore(self.score)
            pygame.mixer.music.pause()
            self.sound_fail.play()
            font = AssetsLoader.getFont("bigfont")
            height = font.get_linesize()
            center,top = screen.get_rect().center
            top -= height//2
            line = font.render(LocaleManager.getString("failure"),1,(255,0,0))
            r = line.get_rect()
            r.midtop = center,top
        else:
            self.game.setHighScore(self.score)
            self.sound_newbest.play()
            font = font = AssetsLoader.getFont("bigfont")
            height = font.get_linesize()
            center,top = screen.get_rect().center
            top -= height//2
            line = font.render(LocaleManager.getString("new_record"),1,(255,0,0))
            r = line.get_rect()
            r.midtop = center,top
        font = AssetsLoader.getFont("midfont")
        text = font.render(LocaleManager.getString("end_score") + str(self.score), 1, (255,255,255))
        top = r.top + r.height + 10
        center = r.center[0]
        r2 = text.get_rect()
        r2.midtop = center,top
        screen.blit(line, r)
        screen.blit(text, r2)
        pygame.display.flip()

    def handle(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.return_to_home = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.finished = 1

    def update(self, game):
        if self.finished:
            game.nextState = Level(self.screen)
        if self.return_to_home:
            game.nextState = Homepage(self.screen)


class Homepage(State):
    def __init__(self, screen : pygame.Surface):
        self.screen = screen
        self.finished = False
        self.button_settings = PushButton(
    942, 42, 40, 40, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), 
    " ")
        self.label_version = LabelBox(842, 42, 100, 40, "v 1.4.0", show_border=True, font = AssetsLoader.getFont("score_font"))
        self.font_big = AssetsLoader.getFont("bigfont")
        self.font_mid = AssetsLoader.getFont("midfont")
        self.bg = AssetsLoader.getImage("background")
        self.icon_settings = AssetsLoader.getImage("icon_settings")
        self.btn_set_pressed = False

    def firstDisplay(self, screen : pygame.Surface):
        # Display only once when the state is created
        self.refreshOnce()
    
    def refreshOnce(self):
        # Function to refresh the titles once
        # Trigger only when the titles are changed
        self.screen.blit(self.bg, (0, 0))

        # Draw the title
        height = self.font_big.get_linesize()
        center, top = self.screen.get_rect().center
        top -= height // 2
        line = self.font_big.render(LocaleManager.getString("title"), 1, (0, 0, 0))
        r = line.get_rect()
        r.midtop = center, top
        self.screen.blit(line, r)
        # Draw the subtitle
        text = self.font_mid.render(LocaleManager.getString("press_continue"), 1, (0,0,0))
        top = r.top + r.height + 10
        center = r.center[0]
        r2 = text.get_rect()
        r2.midtop = center,top
        self.screen.blit(text, r2)
        self.button_settings.draw(self.screen)
        self.label_version.draw(self.screen)
        self.screen.blit(self.icon_settings, (950, 50))
        pygame.display.update()

    def handle(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.finished = 1
        self.btn_set_pressed = self.button_settings.update(event)
        

    def update(self, game):
        # Clear the background
        self.screen.blit(self.bg, (0, 0))
        updates = self.button_settings.draw(self.screen)
        self.screen.blit(self.icon_settings, (950, 50))
        pygame.display.update(updates)
        if self.btn_set_pressed:
            game.nextState = Settings(self.screen)
            self.btn_set_pressed = False
        if self.finished:
            game.nextState = Instruction(self.screen)

class Settings(State):
    def __init__(self, screen : pygame.Surface):
        self.screen = screen
        self.font_big = AssetsLoader.getFont("bigfont")
        self.font_mid = AssetsLoader.getFont("midfont")
        self.bg = AssetsLoader.getImage("background")

        self.finished = False

        self.status_confirmed = False

        # Init elements

        self.label_locale = LabelBox(50, 100, 200, 50, LocaleManager.getString("language"), show_border = False, font=AssetsLoader.getFont("score_font"))

        self.list1 = OptionBox(
    300, 100, 350, 50, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), LocaleManager.getAllNames())
        
        self.label_bgm = LabelBox(50, 200, 200, 50, LocaleManager.getString("bgm_volume"), show_border = False, font=AssetsLoader.getFont("score_font"))

        self.btn_switch = SwitchButton(
    300, 200, 100, 50, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), 
    LocaleManager.getString("on"), LocaleManager.getString("off"), True)
        
        self.gauge1 = Gauge(
    400, 200, 600, 50, (255, 255, 255), (100, 200, 255), 50, 0, 100, True, AssetsLoader.getFont("score_font"))
        
        self.label_sfx = LabelBox(50, 300, 200, 50, LocaleManager.getString("sfx_volume"), show_border = False, font=AssetsLoader.getFont("score_font"))

        self.btn_switch2 = SwitchButton(
    300, 300, 100, 50, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), 
    LocaleManager.getString("on"), LocaleManager.getString("off"), True)
        
        self.gauge2 = Gauge(
    400, 300, 600, 50, (255, 255, 255), (100, 200, 255), 50, 0, 100, True, AssetsLoader.getFont("score_font"))
        
        self.label_gameinfo = LabelBox(50, 400, 200, 50, LocaleManager.getString("game_info"), show_border = False, font=AssetsLoader.getFont("score_font"))

        self.btn_get_latest = PushButton(
    300, 400, 350, 50, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), LocaleManager.getString("get_latest"))
        
        self.btn_view_gh = PushButton(
    650, 400, 350, 50, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), LocaleManager.getString("goto_github"))
        
        self.btn_ok = PushButton(
    0, 718, 512, 50, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), LocaleManager.getString("confirm"))
        
        self.btn_cancel = PushButton(
    512, 718, 512, 50, (255, 255, 255), (100, 200, 255), AssetsLoader.getFont("score_font"), LocaleManager.getString("cancel"))
        
        self.title = LabelBox(0, 0, 1024, 80, LocaleManager.getString("settings"), show_border = False, font=AssetsLoader.getFont("midfont"))

    def firstDisplay(self, screen : pygame.Surface):
        # Display only once when the state is created
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()
    

    def handle(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        selected_option = self.list1.update(event)
        btn_ok_pressed = self.btn_ok.update(event)
        btn_cancel_pressed = self.btn_cancel.update(event)
        btn_switch_on = self.btn_switch.update(event)
        btn_switch2_on = self.btn_switch2.update(event)
        gauge_curr_val = self.gauge1.update(event)
        gauge2_curr_val = self.gauge2.update(event)

        btn_get_latest_pressed = self.btn_get_latest.update(event)
        btn_view_gh_pressed = self.btn_view_gh.update(event)

        if btn_ok_pressed:
            LocaleManager.setLocale(selected_option)
            if btn_switch_on:
                pygame.mixer.music.set_volume(gauge_curr_val/100)
            else:
                pygame.mixer.music.set_volume(0)
            if btn_switch2_on:
                AssetsLoader.setSoundVolume(gauge2_curr_val/100)
            else:
                AssetsLoader.setSoundVolume(0)

            self.status_confirmed = True
            
        if btn_cancel_pressed:
            self.status_confirmed = True

        if btn_get_latest_pressed:
            webbrowser.open("https://github.com/paul-zz/TurtleFamily/releases")

        if btn_view_gh_pressed:
            webbrowser.open("https://github.com/paul-zz/TurtleFamily")


    def update(self, game):
        # Clear the background
        self.screen.blit(self.bg, (0, 0))

        updates = [self.btn_ok.draw(self.screen)]
        updates.append(self.btn_cancel.draw(self.screen))

        updates.append(self.label_locale.draw(self.screen))

        updates.append(self.label_bgm.draw(self.screen))
        updates.append(self.btn_switch.draw(self.screen))
        updates.append(self.gauge1.draw(self.screen))

        updates.append(self.label_sfx.draw(self.screen))
        updates.append(self.btn_switch2.draw(self.screen))
        updates.append(self.gauge2.draw(self.screen))

        updates.append(self.label_gameinfo.draw(self.screen))
        updates.append(self.btn_get_latest.draw(self.screen))
        updates.append(self.btn_view_gh.draw(self.screen))

        updates.append(self.title.draw(self.screen))
        
        updates.extend(self.list1.draw(self.screen))
        pygame.display.update(updates)

        if self.status_confirmed:
            game.nextState = Homepage(self.screen)
            self.status_confirmed = False