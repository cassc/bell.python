# coding: utf-8

from bell import api
import time
import math

offset = (180, 120)

# http://mathworld.wolfram.com/LogarithmicSpiral.html
def gen_spirals():
    a = 1
    b = 0.2
    theta = 0
    degree = math.pi/180
    while True:
        pw = math.e ** (b*theta)
        x = a * math.cos(theta) * pw
        y = a * math.sin(theta) * pw
        yield (x, y)
        theta += 2 * degree

def draw_spiral(ctx):
    x1, y1 = (180, 120)
    start = time.time()
    for (x, y) in gen_spirals():
        x2, y2 = (offset[0] +x, offset[1]+y)
        ctx.display_line(x1, y1, x2, y2)
        print('show line ({}, {}) - ({}, {})'.format(x1, y1, x2, y2))
        x1, y1 = x2, y2
        time.sleep(0.01)
        if (x1, y1) > tuple(i*2 for i in offset) or (x1, y1) < (0, 0):
            break

def draw_bouncing_ball(ctx):
    x, y, r = (10, 10, 10)
    ctx.display_circle(x, y, r, fill=True,clear=True)
    down = True
    u = 10
    
    while x< 340:
        path = range(u, 230)
        if not down:
            path = list(path)
            path.reverse()
        if down:
            for y in path:
                ctx.display_circle(x, y, r, fill=True, clear=True)
                time.sleep(max(0.01 * (240-y) / 240 * x / 100, 0.005))
                x += 0.01
            down = False
            u = u+10
            if u > 230:
                break
        else:
            for y in path:
                ctx.display_circle(x, y, r, fill=True, clear=True)
                time.sleep(max(0.01 * (240-y) / 240 * x /100, 0.005))
                x += 0.05
            down = True
        
def show_all_component():
    ctx = api.BellControl()
    try:
        ctx.init()
        ctx.clear_display()
        # draw_spiral(ctx)
        # time.sleep(2)
        draw_bouncing_ball(ctx)
    finally:
        ctx.close()

show_all_component()
