import pygame
from locals import *

def shadeSurface(surf, shader, args=[]):
    print("hello")
    y=0
    for row in range(surf.get_height()):
        x=0
        for pixel in range(surf.get_height()):
            surf.set_at((x,y),shader(surf.get_at((x,y),*args)))
            x+=1
        y+=1
    return surf

def brightness(color, multiplier):
    return (clamp((color[0]*multiplier),0,255),clamp((color[1]*multiplier),0,255),clamp((color[2]*multiplier),0,255))

def monochrome(color):
    r = color[0]
    g = color[1]
    b = color[2]
    avg = (r+g+b)/3
    return (avg,avg,avg)