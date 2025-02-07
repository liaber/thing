import pygame, sys, math, random
from pygame.math import Vector2

pygame.init()
WIDTH, HEIGHT = 600,400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

def lerp(a, b, t, lerpFunc=lambda x:x):
    return a + (b - a) * lerpFunc(t)

objects = []
class GameObject:
    def __init__(self, pos, size, texture, velo=Vector2(0,0), doPhysics=True):
        self.pos = pos
        self.size = size
        #self.texture = texture
        if isinstance(texture, tuple):
            self.texture = texture
        elif isinstance(texture, str):
            self.texture = pygame.image.load(texture).convert_alpha()
        self.velo = velo
        self.doPhysics = doPhysics
        objects.append(self)

    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
    
    def center(self):
        return Vector2(self.pos.x+(self.size.x/2),self.pos.y+(self.size.y/2))

    def isGrounded(self):
        rect = pygame.Rect(self.pos.x,self.pos.y,self.size.x,self.size.y+2)
        #pygame.draw.rect(screen, (0,255,0), rect)
        for object in objects:
            if object.rect().colliderect(rect) and object != self:
                return True
            
    def onWall(self):
        rect = pygame.Rect(self.pos.x-2,self.pos.y,self.size.x+4,self.size.y)
        for object in objects:
            if object.rect().colliderect(rect) and object != self:
                return True

    def Physics(self, gravity, friction):
        if not self.doPhysics:
            return
        self.velo.x *= friction
        self.pos.x += self.velo.x
        for object in objects:
            if object != self and self.rect().colliderect(object.rect()):
                if self.velo.x > 0:
                    self.pos.x = object.pos.x - self.size.x
                    self.velo.x = 0
                elif self.velo.x < 0:
                    self.pos.x = object.pos.x + object.size.x
                    self.velo.x = 0

        self.velo.y += gravity
        self.pos.y += self.velo.y
        for object in objects:
            if object != self and self.rect().colliderect(object.rect()):
                if self.velo.y > 0:
                    self.pos.y = object.pos.y - self.size.y
                    self.velo.y = 0
                elif self.velo.y < 0:
                    self.pos.y = object.pos.y + object.size.y
                    self.velo.y = 0

    def Draw(self, camera):
        if isinstance(self.texture, tuple):
            pygame.draw.rect(screen, self.texture, pygame.Rect(self.pos.x-camera.pos.x+(WIDTH/2),self.pos.y-camera.pos.y+(HEIGHT/2),self.size.x,self.size.y))
        if isinstance(self.texture, pygame.Surface):
            screen.blit(self.texture,(self.pos.x-camera.pos.x+(WIDTH/2),self.pos.y-camera.pos.y+(HEIGHT/2)))

class Camera:
    def __init__(self, pos, focus, lerpSpeed=0.1, lerpFunc=lambda x:x):
        self.pos = pos
        self.focus = focus
        self.lerpSpeed = lerpSpeed
        self.lerpFunc = lerpFunc

    def Update(self):
        self.pos.x = int(lerp(self.pos.x, self.focus.center().x, self.lerpSpeed, self.lerpFunc))
        self.pos.y = int(lerp(self.pos.y, self.focus.center().y, self.lerpSpeed, self.lerpFunc))

player = GameObject(Vector2(),Vector2(32,32),"player.png")
ground = GameObject(Vector2(0,368),Vector2(600,32),(0,0,0),doPhysics=False)
wall = GameObject(Vector2(300,200),Vector2(32,200),(0,0,0),doPhysics=False)
camera = Camera(Vector2(0,0),player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #screen.fill((255,255,255))

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    #print(player.isGrounded())
    if keys[pygame.K_UP] and player.isGrounded():
        player.velo.y = -15
    if keys[pygame.K_LEFT]:
        dx = -10
    if keys[pygame.K_RIGHT]:
        dy = 10
    player.velo.x = dx+dy

    camera.Update()
    screen.fill((255,255,255))
    for object in objects:
        object.Draw(camera)
        object.Physics(1,0.8)

    pygame.display.update()
    clock.tick(FPS)