# coding: utf-8

# 本例演示使用show_sequence显示mandelbrot图片，其中包含屏幕所有320×240个像素点
# c.f. https://www.geeksforgeeks.org/mandelbrot-fractal-set-visualization-in-python/

from bell import api,ui
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
    c = complex(x, y)
    for i in range(1, 50):
        c = c * c + c0 
        if abs(c) > 2: 
            return rgb_conv(i) 
    return (0, 0, 0)

def draw_mandelbrot():
    ctx = api.BellControl()
    try:
        ctx.init()
        x_point = []
        start= time.time()
        scale = 480
        print('preparing mandelbrot points')
        for x in range(window_size[0]):
            for y in range(window_size[1]):
                r, g, b = mandelbrot(x/scale, y/scale)
                color = "rgb({},{},{})".format(r, g, b)
                x_point.append(ui.make_dot(x, y, color=color))
        print('gen points {} time: {}'.format(len(x_point), time.time() - start))
        # 由于点列数据量较大，直接使用clear_display会导致界面清屏后出现空白界面
        # 使用show_sequence的clear_first参数可避免此情况
        # ctx.clear_display() 
        ctx.show_sequence(x_point, clear_first=True)
        
        time.sleep(40)
    finally:
        ctx.close()


draw_mandelbrot()
