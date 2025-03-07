import pygame
from shaders import *
from pygame.math import Vector2

class Font:
    def __init__(self, font, size):
        self.font = pygame.font.Font(font,size)

    def render(self, text, color):
        return self.font.render(text, True, color)

    def Draw(self, surface, text, pos, color, center=False):
        surf = self.font.render(text, True, color)
        if center:
            surface.blit(surf, Vector2(pos.x-(surf.get_width()/2),pos.y-(surf.get_height()/2)))
        elif not center:
            surface.blit(surf, pos)
    
class Button:
    def __init__(self, pos, borderColor, dropShadow, borderRadius, borderSize, fillColor, icon, onClick, size="auto"):
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
            if self.rect().collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True
                #print("down")
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked == True:
                self.onClick()
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

    def Draw(self, surface):
        
