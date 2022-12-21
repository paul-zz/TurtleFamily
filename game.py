import os,sys,pygame,math
from random import random
from pygame.locals import *

class Turtle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = turtle_image
        self.rect = self.image.get_rect()
        self.initial_rect_width = self.rect.width
        self.initial_rect_height = self.rect.height
        self.speed = 10
        self.addspeed = 2
        self.status = random() # 初始状态，介于0-1之间
        self.scale_big_flag = True # 决定放大还是缩小
        self.drop_flag = False # 决定是否下落
        self.frozen = False # 为True时将冻结
        self.reset()

    def reset(self):
        self.speed = 5
        self.rect.top = -self.rect.height + 100
        self.rect.centerx = screen_size[0]/2
    
    def collide(self,other):
        return self.rect.colliderect(other.rect)

    def freeze(self):
        self.frozen = True

    def placeAfterCollide(self,other):
        self.rect.top = other.rect.top - self.rect.height

    def update(self):
        if not self.frozen:
            if self.drop_flag:
                self.rect.top += self.speed
                self.speed += self.addspeed
                if self.rect.top > screen_size[1]:
                    self.reset()
            else:
                if self.scale_big_flag:
                    self.status += 0.05
                else:
                    self.status -= 0.05
                
                if self.status>1:
                    self.scale_big_flag = False
                elif self.status<0:
                    self.scale_big_flag = True

                self.scale = 1.5*math.cos(3.14/2.5*self.status)
                self.image = pygame.transform.scale(turtle_image,(int(self.initial_rect_width*self.scale),int(self.initial_rect_height*self.scale)))
                self.rect = self.image.get_rect()
                self.rect.centerx = screen_size[0]/2
        

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.image = pygame.transform.scale(ground_image,(screen_size[0],50))
        self.rect = self.image.get_rect()
        self.rect.top = screen_size[1]-self.rect.height

class State:

    def handle(self,event):
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()

    def firstDisplay(self,screen):
        screen.blit(bg,(0,0))#screen.fill(bg)
        pygame.display.flip()

    def display(self,screen):
        pass

class Level(State):

    def __init__(self):
        pygame.mixer.music.unpause()
        self.firstTurtle = Turtle()
        self.turtlelst = []
        self.turtlelst.append(self.firstTurtle)
        self.sprites = pygame.sprite.RenderUpdates()
        self.ground = Ground()
        self.sprites.add(self.firstTurtle)
        self.sprites.add(self.ground)
        self.score = 0
        self.layer = 0

    def handle(self,event):
        if event.type==QUIT: 
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            touchsound.play()
            self.turtlelst[-1].drop_flag = True

    def update(self,game):
        self.sprites.update()
        score_font = pygame.font.Font('font.ttf',20)
        score_text = score_font.render("得分:"+str(self.score),True,(0,0,0))
        highscore_text = score_font.render("最高分:"+str(highscore),True,(0,0,0))
        screen.blit(score_text,(5,5))
        screen.blit(highscore_text,(screen_size[0]-100,5))
        pygame.display.update()
        
        if self.firstTurtle.collide(self.ground) and not self.firstTurtle.frozen:
            self.firstTurtle.freeze()
            self.firstTurtle.placeAfterCollide(self.ground)
            self.turtlelst.append(Turtle())
            self.sprites.add(self.turtlelst[-1])
            self.score += 1
            self.layer += 1

        if self.turtlelst[-1] != self.firstTurtle:
            if self.turtlelst[-1].collide(self.turtlelst[-2]) and not self.turtlelst[-1].frozen:
                self.turtlelst[-1].freeze()
                self.turtlelst[-1].placeAfterCollide(self.turtlelst[-2])
                if self.turtlelst[-1].rect.width > self.turtlelst[-2].rect.width: # GO DIE MOTHERFUCKER
                    nextstate = GameOver(self.score)
                    game.nextState = nextstate
                else: # CONTINUE
                    self.score += self.layer
                    self.layer += 1
                    eps = (self.turtlelst[-2].rect.width - self.turtlelst[-1].rect.width)/self.turtlelst[-2].rect.width # error of the width between two turtles
                    if eps<0.1:
                        text=font1.render("太厉害了",True,(0,0,0))
                        sound = liuliuliu
                        self.score += 5
                        if eps<0.05:
                            text=font1.render("真是神准",True,(0,0,0))
                            sound = liupi
                            self.score += 10
                        sound.play()
                        height = font1.get_linesize()
                        center,top = screen.get_rect().center
                        top-= height
                        r=text.get_rect()
                        r.midtop = center,top
                        #sprites.clear(screen,clear_callback)
                        screen.blit(bg,(0,0))#screen.fill(bg)
                        self.sprites.update()
                        updates = self.sprites.draw(screen)
                        screen.blit(text,r)
                        screen.blit(score_text,(5,5))
                        screen.blit(highscore_text,(screen_size[0]-100,5))
                        pygame.display.update()
                        pygame.time.delay(1000)
                        screen.blit(bg,(0,0))#screen.fill(bg)
                        updates = self.sprites.draw(screen)
                        pygame.display.update(updates)
                        #text=font1.render("                 ",True,(0,0,0),(255,255,255))

                        #screen.blit(text,r)
                        pygame.display.update()
                    self.turtlelst.append(Turtle())
                    self.sprites.add(self.turtlelst[-1])
    
    def display(self, screen):
        screen.blit(bg,(0,0))#screen.fill(bg)
        updates = self.sprites.draw(screen)
        pygame.display.update(updates)
        pygame.time.Clock().tick(75)

class Paused(State):
    finished = 0
    image = None
    text = ''

    def handle(self,event):
        State.handle(self,event)
        if event.type in [MOUSEBUTTONDOWN,KEYDOWN]:
            self.finished = 1

    def update(self,game):
        if self.finished:
            game.nextState = self.nextState()


class Instruction(Paused):
    nextState = Level
    
    def firstDisplay(self,screen):
        screen.blit(bg,(0,0))#screen.fill(bg)
        font = pygame.font.Font('font.ttf',80)#pygame.font.SysFont('droidsansfallback', 50)
        height = font.get_linesize()
        center,top = screen.get_rect().center
        top -= height//2
        line = font.render('不可以比下面的乌龟大哦',1,(0,0,0))
        r = line.get_rect()
        r.midtop = center,top
        screen.blit(line, r)
        pygame.display.flip()
        letsplay.play()
        pygame.time.delay(1000)
        screen.blit(bg,(0,0))#screen.fill(bg)
        line1 = font.render('Ready',1,(255,0,0)) 
        r = line1.get_rect()
        r.midtop = center,top
        screen.blit(line1,r)
        pygame.display.flip()
        ready.play()
        pygame.time.delay(500)
        screen.blit(bg,(0,0))#screen.fill(bg)
        line2 = font.render('GO!',1,(255,0,0))
        r = line1.get_rect()
        r.midtop = center,top
        screen.blit(line2,r)
        pygame.display.flip()
        pygame.time.delay(500)
        self.finished = 1

class Homepage(Paused):
    nextState = Instruction

    def firstDisplay(self,screen):
        screen.blit(bg,(0,0))#screen.fill(bg)
        font = pygame.font.Font('font.ttf',100)#pygame.font.SysFont('droidsansfallback', 50)
        height = font.get_linesize()
        center,top = screen.get_rect().center
        top -= height//2
        line = font.render('乌龟家族',1,(0,0,0))
        r = line.get_rect()
        r.midtop = center,top
        screen.blit(line, r)
        pygame.display.flip()


class GameOver(Paused):
    nextState = Level

    def __init__(self, score):
        self.score = score

    def firstDisplay(self,screen):
        global highscore
        if self.score <= highscore or highscore==0:
            if highscore ==0:
                highscore = self.score
            pygame.mixer.music.pause()
            dededon.play()
            font = pygame.font.Font('font.ttf',100)#pygame.font.SysFont('droidsansfallback', 50)
            height = font.get_linesize()
            center,top = screen.get_rect().center
            top -= height//2
            line = font.render('太可惜了',1,(255,0,0))
            r = line.get_rect()
            r.midtop = center,top
        else:
            highscore = self.score
            newbest.play()
            font = pygame.font.Font('font.ttf',100)#pygame.font.SysFont('droidsansfallback', 50)
            height = font.get_linesize()
            center,top = screen.get_rect().center
            top -= height//2
            line = font.render('新的记录！',1,(255,0,0))
            r = line.get_rect()
            r.midtop = center,top
        font = pygame.font.Font('font.ttf',50)
        text = font.render('得分：'+str(self.score),1,(255,255,255))
        top = r.top + r.height+10
        center = r.center[0]
        r2 = text.get_rect()
        r2.midtop = center,top
        screen.blit(line, r)
        screen.blit(text, r2)
        pygame.display.flip()

class Game:
    def __init__(self):
        self.state = None
        self.nextState = Homepage()

    def run(self):
        pygame.init()

        # display initiation
        global screen_size,screen
        screen_size = (1024,768)
        screen = pygame.display.set_mode(screen_size)
        global bg
        bg = pygame.image.load('bg.png')
        bg = bg.convert()
        bg = pygame.transform.scale(bg,(screen_size[0],screen_size[1]))
        pygame.mouse.set_visible(1)
        pygame.display.set_caption('Turtle Family')
        
        #fonts initiation
        global font1
        font1 = pygame.font.Font('font.ttf',100)#pygame.font.SysFont('droidsansfallback', 50)

        #image initiation
        global turtle_image,ground_image
        turtle_image = pygame.image.load('turtle.png')
        turtle_image = turtle_image.convert_alpha()
        ground_image = pygame.image.load('ground.png')
        ground_image  =ground_image.convert()
        
        #sound initiation
        global touchsound,liupi,liuliuliu,dededon,newbest,letsplay,ready
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        touchsound = pygame.mixer.Sound("touch.wav")
        liupi = pygame.mixer.Sound("liupi.wav")
        liuliuliu = pygame.mixer.Sound("666.wav")
        dededon = pygame.mixer.Sound("dededon.wav")
        newbest = pygame.mixer.Sound("newbest.wav")
        ready = pygame.mixer.Sound("ready.wav")
        letsplay = pygame.mixer.Sound("letsplay.wav")

        #FPS initiation
        pygame.time.Clock().tick(60)

        #highscore initiation
        global highscore
        highscore = 0

        #Main loop
        while True:
            if self.state != self.nextState:
                self.state = self.nextState
                self.state.firstDisplay(screen)
            for event in pygame.event.get():
                self.state.handle(event)
            self.state.update(self)
            self.state.display(screen)


if __name__ == '__main__':
    game = Game()
    game.run()


'''

font1 = pygame.font.Font('font.ttf',100)#pygame.font.SysFont('droidsansfallback', 50)



turtle_image = pygame.image.load('turtle.png')
turtle_image = turtle_image.convert()
ground_image = pygame.image.load('turtle.png')
ground_image  =ground_image.convert()

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1)
touchsound = pygame.mixer.Sound("touch.wav")
pygame.time.Clock().tick(60)
if __name__ == '__main__':
    game = Game()
    game.run()

turtle = Turtle()
ground = Ground()
turtlelst = []

turtlelst.append(turtle)
sprites = pygame.sprite.RenderUpdates()
sprites.add(turtlelst)
sprites.add(ground)

screen = pygame.display.get_surface()
bg = (255,255,255)
screen.fill(bg)
pygame.display.flip()

def clear_callback(surf,rect):
    surf.fill(bg,rect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            touchsound.play()
            turtlelst[-1].drop_flag = True

    if turtle.collide(ground) and not turtle.frozen:
        turtle.freeze()
        turtle.placeAfterCollide(ground)
        turtlelst.append(Turtle())
        sprites.add(turtlelst[-1])

    if turtlelst[-1] != turtle:
        if turtlelst[-1].collide(turtlelst[-2]) and not turtlelst[-1].frozen:
            turtlelst[-1].freeze()
            turtlelst[-1].placeAfterCollide(turtlelst[-2])
            if turtlelst[-1].rect.width > turtlelst[-2].rect.width: # GO DIE
                break
            else: # CONTINUE
                eps = (turtlelst[-2].rect.width - turtlelst[-1].rect.width)/turtlelst[-2].rect.width
                if eps<0.1:
                    text=font1.render("太给力了",True,(0,0,0),(255,255,255))
                    if eps<0.05:
                        text=font1.render("真是神准",True,(0,0,0),(255,255,255))
                    height = font1.get_linesize()
                    center,top = screen.get_rect().center
                    top-= height
                    r=text.get_rect()
                    r.midtop = center,top
                    #sprites.clear(screen,clear_callback)
                    sprites.update()
                    updates = sprites.draw(screen)
                    screen.blit(text,r)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    text=font1.render("                 ",True,(0,0,0),(255,255,255))
                    screen.blit(text,r)
                    pygame.display.update()
                
                turtlelst.append(Turtle())
                sprites.add(turtlelst[-1])

    sprites.clear(screen,clear_callback)
    sprites.update()
    pygame.time.Clock().tick(60)
    updates = sprites.draw(screen)
    pygame.display.update(updates)
'''
