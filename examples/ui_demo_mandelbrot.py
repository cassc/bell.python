# coding: utf-8

# c.f. https://www.geeksforgeeks.org/mandelbrot-fractal-set-visualization-in-python/

from bell import api
import time
from numpy import complex, array 
import colorsys 


window_size = (320, 240)

# a function to return a tuple of colors 
# as integer value of rgb 
def rgb_conv(i): 
    color = 255 * array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 0.5)) 
    return tuple(color.astype(int)) 
  
# function defining a mandelbrot 
def mandelbrot(x, y): 
    c0 = complex(x, y) 
    c = 0
    for i in range(1, 1000): 
        if abs(c) > 2: 
            return rgb_conv(i) 
        c = c * c + c0 
    return (0, 0, 0)


def draw_mandelbrot():
    ctx = api.BellControl()
    try:
        ctx.init()
        
        x_point = []
        scale = 25
        for x in range(window_size[0]*scale):
            if x%scale != 0:
                continue
            for y in range(window_size[1]*100):
                if y%scale != 0:
                    continue
                r, g, b = mandelbrot(x, y)
                if (r,g,b) != (0,0,0):
                    color = "rgb({},{},{})".format(r, g, b)
                    x_point.append(api.make_dot(x/scale, y/scale, color=color))
        ctx.clear_display()
        ctx.show_sequence(x_point)
        time.sleep(40)
    finally:
        ctx.close()


draw_mandelbrot()
