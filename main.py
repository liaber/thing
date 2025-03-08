import pygame, sys, math, UI
from pygame.math import Vector2
from shaders import *
from locals import *

WIDTH, HEIGHT, SCALE = 600, 300, 3
pygame.init()
screen = pygame.Surface((WIDTH,HEIGHT))
display = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE),vsync=1)
clock = pygame.time.Clock()
fps = 0
dt = 0 #Delta time
t = 0 #Time in milliseconds

if getattr(pygame, "IS_CE", False) == False:
    raise ImportError("This script requires pygame-ce!")

def mousePos():
    global SCALE
    return Vector2(pygame.mouse.get_pos())/SCALE

'''def loadLevel(level, tileset):
    global object, player
    with open(f'{PATH}Levels/{level}') as txt:
        level = txt.read()
    objects = []
    level = level.split("\n")
    map = []
    for row in level:
        map.append(list(row.split(",")))
    y=0
    for row in map:
        x=0
        for tile in row:
            if tile != "-1":
                if tile == "4":
                    Object(Vector2(x*TILESIZE, y*TILESIZE),Vector2(TILESIZE),texture=tileset.tiles[tile],collider=False)
                else:
                    Object(Vector2(x*TILESIZE, y*TILESIZE),Vector2(TILESIZE),texture=tileset.tiles[tile])
            print(objects)
            x+=1
        y+=1
    player.pos=Vector2(TILESIZE*2)
    objects.append(player)'''

'''def Draw(camera):
    playerOverlap = []
    for object in objects:
        if object.pos.y < player.pos.y and object != player.weapon:
            object.Draw(camera)
    for object in objects:
        if object.pos.y >= player.pos.y+14 and object != player.weapon and object != player:
            object.Draw(camera)
        else:
            playerOverlap.append(object)
    for object in playerOverlap:
        object.Draw(camera)
    player.Draw(camera)
    player.weapon.Draw(camera)'''
    
def WorldToScreenPoint(camera, point):
    return (point - camera.pos)

def ScreenToWorldPoint(camera, point):
    return (point + camera.pos)

class AnimationController:
    def __init__(self, spriteSheet, spriteSize, animation=0, frame=0, frameGap=175):
        #Load all animations
        self.animations = []
        spriteSheet = pygame.image.load(spriteSheet).convert_alpha()
        for y in range(int(spriteSheet.get_height()/spriteSize.y)):
            newAnim = []
            for x in range(int(spriteSheet.get_width()/spriteSize.x)):
                newFrame = pygame.Surface(spriteSize)
                newFrame.set_colorkey((0,0,0))
                newFrame.blit(spriteSheet,Vector2(-x*spriteSize.x, -y*spriteSize.y))
                newAnim.append(newFrame)
            self.animations.append(newAnim)

        self.animation = animation
        self.frame = frame
        self.frameGap = frameGap
        self.flipX = False
        self.flipY = False

    def Update(self,time,dt):
        self.UpdateFrame(time,dt)
        #Add code for changing animations through class inheritance

    def UpdateFrame(self, time, dt):
        #self.animations[animation number][frame number]
        if (time - dt) // self.frameGap != time // self.frameGap:
            self.frame += 1
            if self.frame+1 > len(self.animations[self.animation]):
                self.frame = 0

    def getFrame(self):
        frame = self.animations.copy()[self.animation][self.frame]
        frame = pygame.transform.flip(frame,self.flipX,self.flipY)
        return frame
    
    def SetAnimation(self, animation):
        if self.animation != animation:
            self.animation = animation
            self.frame = 0

objects = []
class Object:
    def __init__(self, pos, size, velo=Vector2(), texture=(255,0,0), collider=True, doPhysics=True ,rot=0):
        self.pos = pos
        self.size = size
        self.velo = velo
        if isinstance(texture, str):
            self.texture = pygame.image.load(texture).convert_alpha()
        else:
            self.texture = texture
        
        self.collider = collider
        self.doPhysics = doPhysics
        self.rot = rot
        objects.append(self)

    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
    
    def center(self):
        return Vector2(self.pos.x+(self.size.x/2),self.pos.y+(self.size.y/2))
    
    def SetCenter(self, pos):
        self.pos = pos - (self.size/2)
    
    def Draw(self, camera):
        if isinstance(self, AnimationController):
            screen.blit(pygame.transform.rotate(self.getFrame(),math.degrees(self.rot)), ((int(self.pos.x)-int(camera.pos.x)),(int(self.pos.y)-int(camera.pos.y))))
        elif isinstance(self.texture, tuple):
            pygame.draw.rect(screen, self.texture, pygame.Rect((int(self.pos.x)-int(camera.pos.x)),(int(self.pos.y)-int(camera.pos.y)),self.size.x,self.size.y))
        elif isinstance(self.texture, pygame.Surface):
            screen.blit(pygame.transform.rotate(self.texture,math.degrees(-self.rot)), self.pos-camera.pos)

    def Physics(self, gravity, friction, dt):
        if self.collider == True and self.doPhysics == True:
            self.velo.x *= 1/(1+(friction*dt))
            self.pos.x += self.velo.x*dt
            for object in objects:
                if object != self and object.rect().colliderect(self.rect()) and object.collider == True:
                    if self.velo.x > 0:
                        self.pos.x = object.pos.x - self.size.x
                        self.velo.x
                    if self.velo.x < 0:
                        self.pos.x = object.pos.x + object.size.x

            self.velo.y += gravity*dt
            self.pos.y += self.velo.y*dt
            for object in objects:
                if object != self and object.rect().colliderect(self.rect()) and object.collider == True:
                    if self.velo.y > 0:
                        self.pos.y = object.pos.y - self.size.y
                        self.velo.y = 0
                    if self.velo.y < 0:
                        self.pos.y = object.pos.y + object.size.y
                        self.velo.y = 0

class Light(Object, AnimationController):
    def __init__(self, pos, size, spriteSheet, weapon=None, velo=Vector2(), texture=(255,0,0), animation=0, frame=0, frameGap=250, spriteSize=Vector2(0,0),collider=True):
        Object.__init__(self,pos,size,velo,texture,collider)
        AnimationController.__init__(self,spriteSheet,spriteSize,animation,frame,frameGap)

class Player(Object, AnimationController):
    def __init__(self, pos, size, spriteSheet, weapon=None, velo=Vector2(), texture=(255,0,0), animation=0, frame=0, frameGap=150, spriteSize=Vector2(0,0),collider=True):
        Object.__init__(self,pos,size,velo,texture,collider)
        AnimationController.__init__(self,spriteSheet,spriteSize,animation,frame,frameGap)
        #self.weapon = weapon

    def isGrounded(self):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y+1)
        for object in objects:
            if object != self and rect.colliderect(object.rect()):
                return True
        return False
    
    def SetAnimation(self, animation):
        if self.animation != animation:
            self.animation = animation
        

    def Update(self,time,dt):
        self.UpdateFrame(time,dt)
        if self.velo.x > 0:
            self.flipX = False
        if self.velo.x < 0:
            self.flipX = True
        if self.isGrounded():
            if abs(self.velo.x) > 0.1:
                self.SetAnimation(1)
            else:
                self.SetAnimation(0)
        else:
            if abs(self.velo.x) > 0.1:
                self.SetAnimation(3)
            else:
                self.SetAnimation(2)

class Camera:
    def __init__(self, pos, focus, lerp=lambda x:x, speed=0.7):
        self.pos = pos
        self.focus = focus
        self.lerp = lerp
        self.speed = speed

    def Update(self, dt):
        self.pos.x = lerp(self.pos.x, self.focus.center().x+(self.focus.velo.x*WIDTH)-(WIDTH/2), self.speed*(dt/1000), self.lerp)
        self.pos.y = lerp(self.pos.y, self.focus.center().y+(self.focus.velo.y*HEIGHT)-(HEIGHT/2), (self.speed*(dt/1000)*(WIDTH/HEIGHT)), self.lerp)

'''class TileSet:
    def __init__(self, set, tileSize=TILESIZE):
        self.tiles = {}
        set = pygame.image.load(f'{PATH}Assets/{set}').convert_alpha()
        for i in range(int(set.get_width()/tileSize)):
            surf = pygame.Surface(Vector2(tileSize))
            surf.set_colorkey((0,0,0))
            surf.blit(set,Vector2(-i*tileSize,0))
            self.tiles[f'{i}'] = surf.copy()'''

'''class Weapon(Object, AnimationController):
    def __init__(self, pos, size, spriteSheet, type, damage, range, bulletImg=None, velo=Vector2(), texture=(255,0,0), animation=0, frame=0, frameGap=175, spriteSize=Vector2(TILESIZE),collider=False):
        Object.__init__(self,pos,size,velo,texture,collider)
        AnimationController.__init__(self,spriteSheet,spriteSize,animation,frame,frameGap)
        self.type = type
        self.damage = damage
        self.range = range
        if self.type == 'ranged':
            self.bullets = []
            self.bulletImg = bulletImg
        

    def Attack(self):
        if self.type == 'melee':
            self.SetAnimation(1)
        if self.type == 'ranged':
            self.SetAnimation(1)

    def Update(self, time, dt):
        if self.animation == 1 and self.frame == len(self.animations[self.animation])-1:
            self.SetAnimation(0)
        if self.type == 'ranged':
            dir = WorldToScreenPoint(camera, self.center()) - Vector2(pygame.mouse.get_pos())
            self.rot = math.atan((-dir.y)/dir.x)+(math.pi)
            if dir.x < 0:
                self.rot += math.pi
            self.SetCenter(Vector2(math.cos(-self.rot)*15,math.sin(-self.rot)*15)+player.center())
            ''''''if self.rot >= math.pi/2 and self.rot <= math.pi*1.5:
                self.flipX = True
            else:
                self.flipX = False''''''
        self.UpdateFrame(time, dt)'''


#WORK ON UI
#tileset = TileSet("tileset.png")

#wall = Object(Vector2(16,16),Vector2(16,16),texture=tileset.tiles[0])

player = Player(Vector2(0,0),Vector2(16,32),"player.png",spriteSize=Vector2(16,32))
ground = Object(Vector2(0,100),Vector2(1000,20),doPhysics=False)

camera = Camera(Vector2(0,0),player,speed=1)#lambda x:-(x**2)+(x*2)

headerFont = UI.Font("yoster.ttf", 40)
subtextFont = UI.Font("yoster.ttf", 12)

#loadLevel("1.csv",tileset)
def level():
    global dt, t
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #player.weapon.Attack()

        keys = pygame.key.get_pressed()
        x = 0
        if keys[pygame.K_UP] and player.isGrounded():
            player.velo.y = -.3
        if keys[pygame.K_LEFT]:
            x -= 0.25
        if keys[pygame.K_RIGHT]:
            x += 0.25
        player.velo.x = x
        
        
        camera.Update(dt)
        screen.fill((45,51,66))
        for object in objects:
            object.Physics(.001, 0.1, dt)
            if isinstance(object, AnimationController):
                object.Update(t,dt)
            object.Draw(camera)
        surface = pygame.Surface((64,64))
        pygame.draw.circle(surface, brightness((163, 143, 15),1), (32,32), 8)
        surface = pygame.transform.gaussian_blur(surface, 8)
        screen.blit(surface, (100,100), special_flags=pygame.BLEND_RGB_ADD)
        #Draw(camera)

        #pygame.draw.circle(screen, (255,0,0), WorldToScreenPoint(camera, player.weapon.center()),5)
        #pygame.draw.circle(screen, (0,0,255), Vector2(pygame.mouse.get_pos()),5)
        #print(player.velo.y)
        display.blit(pygame.transform.scale_by(screen, SCALE),(0,0))
        pygame.display.update()
        dt = clock.tick(fps)
        t += dt

def mainMenu():
    global dt, t
    #playButton = UI.Button(Vector2(300,200),Vector2(100,30),(255,255,255),0.1,7,2,(0,0,0),"Play!","yoster.ttf",level)
    #playButton = UI.Button(Vector2(300,200),(255,255,255),0.1,7,2,(0,0,0),("Play!",25),"yoster.ttf",level)
    #playButton = UI.Button(Vector2(300,200),(255,255,255),0.1,7,2,(0,0,0),,"yoster.ttf",level)
    playButton = UI.Button(Vector2(300,200),(255,255,255),0.1,7,2,(0,0,0),"play.png",levels)
    settingsButton = UI.Button(Vector2(270,200),(255,255,255),0.1,7,2,(0,0,0),"settings.png",settings)
    while True:
        events = pygame.event.get()
        for event in events:
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        mouse = pygame.mouse.get_pressed()
    
        screen.fill((45,51,66))

        headerFont.Draw(screen, "Game Title", Vector2(300,75), (255,255,255), True)
        playButton.Update(events, mousePos())
        playButton.Draw(screen)
        settingsButton.Update(events, mousePos())
        settingsButton.Draw(screen)
        #pygame.draw.circle(screen, (0,255,0), mousePos(), 5)

        display.blit(pygame.transform.scale_by(screen, SCALE),(0,0))
        pygame.display.update()
        dt = clock.tick(30)
        t += dt

def levels():
    global dt, t
    levelButtons = [UI.Button(Vector2(32*(i+1),64),(255,255,255),0.1,7,2,(0,0,0),(str(i+1),16,"yoster.ttf"),level,size=Vector2(24,24)) for i in range(5)]
    backButton = UI.Button(Vector2(16,16),(255,255,255),0.1,7,2,(0,0,0),"leftArrow.png",mainMenu)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        screen.fill((45,51,66))
        for button in levelButtons:
            button.Update(events,mousePos())
            button.Draw(screen)
        backButton.Update(events,mousePos())
        backButton.Draw(screen)

        display.blit(pygame.transform.scale_by(screen, SCALE),(0,0))
        pygame.display.update()
        dt = clock.tick(30)
        t += dt

def settings():
    global dt, t

    backButton = UI.Button(Vector2(16,16),(255,255,255),0.1,7,2,(0,0,0),"leftArrow.png",mainMenu)
    displaySettingsButton = UI.Button(Vector2(300,110), (255,255,255), 0.1, 7, 2, (0,0,0), ("Display Settings",16,"yoster.ttf"),displaySettings)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((45,51,66))

        headerFont.Draw(screen, "Settings", Vector2(300,50), (255,255,255), center=True)
        backButton.Update(events,mousePos())
        backButton.Draw(screen)
        displaySettingsButton.Update(events,mousePos())
        displaySettingsButton.Draw(screen)

        display.blit(pygame.transform.scale_by(screen, SCALE),(0,0))
        pygame.display.update()
        dt = clock.tick(30)
        t += dt        

def displaySettings():
    global dt, t

    backButton = UI.Button(Vector2(16,16),(255,255,255),0.1,7,2,(0,0,0),"leftArrow.png",settings)
    displaySizeSlider = UI.Slider(Vector2(350,125),1,100,(1,3),brightness((255,255,255),.7),(255,255,255),2,increment=1)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((45,51,66))

        headerFont.Draw(screen, "Display Settings", Vector2(300,50), (255,255,255), center=True)
        backButton.Update(events,mousePos())
        backButton.Draw(screen)

        displaySizeSlider.Draw(screen)
        displaySizeSlider.Update(screen, mousePos(), events)
        subtextFont.Draw(screen, "Display Size:", Vector2(250,125), (255,255,255), center=True)

        display.blit(pygame.transform.scale_by(screen, SCALE),(0,0))
        pygame.display.update()
        dt = clock.tick(30)
        t += dt

mainMenu()