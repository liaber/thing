import pygame
from shaders import *
from pygame.math import Vector2
from locals import *

class Box:
    def __init__(self, pos, size, color, borderColor, dropShadow, borderRadius, borderWidth):
        self.pos = pos
        self.size = size
        self.color = color
        self.borderColor = borderColor
        self.dropShadow = dropShadow
        self.borderRadius = borderRadius
        self.borderWidth = borderWidth
        
    def Draw(self, surface):
        rect = self.rect()
        rect = pygame.Rect(rect.left+2,rect.top+2,rect.width,rect.height)
        pygame.draw.rect(surface, brightness(self.borderColor,self.dropShadow), rect, border_radius=self.borderRadius)
        pygame.draw.rect(surface, self.color, self.rect(), border_radius=self.borderRadius)
        pygame.draw.rect(surface, self.borderColor, self.rect(), border_radius=self.borderRadius, width=self.borderWidth)

    def rect(self):
        return pygame.Rect(self.pos, self.size)

class Font:
    def __init__(self, font, size):
        self.font = pygame.font.Font(font,size)

    def render(self, text, color):
        return self.font.render(text, False, color)

    def Draw(self, surface, text, pos, color, center=False):
        surf = self.font.render(text, False, color)
        if center:
            surface.blit(surf, Vector2(pos.x-(surf.get_width()/2),pos.y-(surf.get_height()/2)))
        elif not center:
            surface.blit(surf, pos)
    
class Button:
    def __init__(self, pos, borderColor, dropShadow, borderRadius, borderSize, fillColor, icon, onClick, size="auto", runArgs=[]):
        self.pos = pos
        self.borderColor = borderColor
        self.dropShadow = dropShadow
        self.borderRadius = borderRadius
        self.borderSize = borderSize
        self.fillColor = fillColor
        try:
            self.text = icon[0]
            self.font = Font(icon[2], icon[1])
            self.icon = self.font.render(self.text, self.borderColor)
        except:
            self.icon = pygame.image.load(icon).convert_alpha()
                
        if size == "auto":
            padding = min(self.icon.get_width(), self.icon.get_height())*0.5
            padding = Vector2(padding,padding)
            self.size = Vector2(self.icon.get_width(), self.icon.get_height())+padding
        else:
            self.size = size

        self.clicked = False
        self.onClick = onClick
        self.runArgs = runArgs

    def Draw(self, surface):

        rect = self.rect()
        rect = pygame.Rect(rect.left+2,rect.top+2,rect.width,rect.height)

        if self.clicked  == True:
            pygame.draw.rect(surface, self.fillColor, rect, border_radius=self.borderRadius)
            pygame.draw.rect(surface, self.borderColor, rect, width=self.borderSize, border_radius=self.borderRadius)
            surface.blit(self.icon, self.pos-(Vector2(self.icon.get_size())/2)+Vector2(2,2))

        if self.clicked == False:
            pygame.draw.rect(surface, brightness(self.borderColor, self.dropShadow), rect, border_radius=self.borderRadius)
            pygame.draw.rect(surface, self.fillColor, self.rect(), border_radius=self.borderRadius)
            pygame.draw.rect(surface, self.borderColor, self.rect(), width=self.borderSize, border_radius=self.borderRadius)
            surface.blit(self.icon, self.pos-(Vector2(self.icon.get_size())/2))

    def Update(self, events, mousePos):
        for event in events:
            #print(event)
            if self.rect().collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = True
                #print("down")
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked == True:
                self.onClick(*self.runArgs)
                #print("up")

    def rect(self):
        return pygame.Rect(self.pos.x-(self.size.x/2), self.pos.y-(self.size.y/2), self.size.x, self.size.y)
    
class Slider:
    def __init__(self, pos, sliderPos, displayWidth, range, lineColor, sliderColor, borderRadius, sliderBorderColor=False, increment=0.1):
        self.pos = pos
        self.sliderPos = sliderPos
        self.displayWidth = displayWidth
        self.range = range
        self.lineColor = lineColor
        self.sliderColor = sliderColor
        self.borderRadius = borderRadius
        if sliderBorderColor == False:
            self.sliderBorderColor = sliderColor
        else:
            self.sliderBorderColor = sliderBorderColor
        self.increment = increment
        self.selected = False

    def Draw(self, surface):
        displaySurf = pygame.Surface((self.displayWidth+4,8),flags=pygame.SRCALPHA)
        lineRect = pygame.Rect(2,2,self.displayWidth,4)
        pygame.draw.rect(displaySurf, self.lineColor, lineRect, border_radius=self.borderRadius)
        pygame.draw.rect(displaySurf, self.sliderColor, self.sliderRect(), border_radius=self.borderRadius)
        pygame.draw.rect(displaySurf, self.sliderBorderColor, self.sliderRect(), border_radius=self.borderRadius, width=1)
        surface.blit(displaySurf, self.pos-(Vector2(displaySurf.get_width(),displaySurf.get_height())/2))
        
    def sliderRect(self):
        return pygame.Rect((mapRange(self.range,(0,self.displayWidth),self.sliderPos)),0,4,8)
    
    def rect(self):
        refRect = self.sliderRect()
        return pygame.Rect(refRect.left+self.pos.x-((self.displayWidth+4)/2),self.pos.y-4,4,8)

    def Update(self, screen, mousePos, events):
        #pygame.draw.rect(screen, (255,0,0), self.rect())
        for event in events:
            if self.rect().collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.selected = True
                #print("down")
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selected == True:
                self.selected = False
                self.sliderPos = roundIncrement(self.sliderPos, self.increment)

        #print(self.selected)

        if self.selected == True:
            self.sliderPos = mapRange((self.pos.x,self.pos.x+self.displayWidth),self.range,clamp(mousePos.x+self.displayWidth/2,self.pos.x,self.pos.x+self.displayWidth))

    def get(self):
        try:
            return round(roundIncrement(self.sliderPos, self.increment), len(str(self.increment).split(".")[1]))
        except:
            return roundIncrement(self.sliderPos, self.increment)