def clamp(num, min, max):
    if num > max: return max
    if num < min: return min
    return num

def brightness(color, multiplier):
    return (clamp((color[0]*multiplier),0,255),clamp((color[1]*multiplier),0,255),clamp((color[2]*multiplier),0,255))

def monochrome(color):
    r = color[0]
    g = color[1]
    b = color[2]
    avg = (r+g+b)/3
    return (avg,avg,avg)