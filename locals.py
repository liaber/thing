import json
from pygame.math import Vector2

def clampVec2(vec, max):
    if vec.length() == 0:
        return Vector2(0,0)
    l = vec.length()
    f = min(l,max)/l
    return vec*f

def lerp(a, b, t, curve=lambda x:x):
    return a + (b - a) * curve(t)

def mapRange(a, b, s):
    return b[0]+(((s-a[0])*(b[1]-b[0]))/(a[1]-a[0]))

def roundIncrement(a,i):
    a /= i
    a = round(a)
    a *= i
    return a

def clamp(num, min, max):
    if num > max: return max
    if num < min: return min
    return num

def loadFile(file):
    type = file.split(".")[1]
    if type == "json":
        with open(file, "r") as f:
            data = json.load(f)
            return data
        
def writeFile(file, data):
    type = file.split(".")[1]
    if type == "json":
        with open(file, "w") as f:
            json.dump(data, f, indent=4)